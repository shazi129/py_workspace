"""教学类 Manim 场景的通用主题与动画组件。

具体教学场景继承 :class:`TeachingScene` 后，可以直接使用统一的背景、
中文字体、字幕、章节标题、高亮和清场动画。例如::

    class MyLesson(TeachingScene):
        def construct(self):
            title = self.section_title("示例章节")
            self.play(FadeIn(title))
            self.set_subtitle("这是一条字幕", duration=2)

这里的颜色常量也会由 ``common`` 包统一导出，供具体场景复用。
"""

from manim import *


# 深色背景和教学动画中常用的语义色。
BG = "#10151C"
ACCENT = "#F5C451"       # 标题、重点和主要强调色
BLUE_ACCENT = "#4DB6E7"  # 初始对象或被除数
GREEN_ACCENT = "#69D39B" # 结果、结论或正确状态
PINK_ACCENT = "#F08080"  # 辅助框选和对比强调


class TeachingScene(Scene):
    """教学动画的基础场景。

    子类只需要实现 ``construct``。Manim 会在 ``construct`` 前自动调用
    :meth:`setup`，因此背景、默认字体和字幕状态不需要在子类重复初始化。

    Attributes:
        animation_slowdown: 所有 ``self.play`` 动画的时长倍率。大于 1 会
            放慢动画，小于 1 会加快动画。
        default_font: ``Text`` 使用的默认字体，应为系统中已安装的字体。
        subtitle: 当前仍在画面中的字幕组；没有字幕时为 ``None``。
    """

    animation_slowdown = 1.25
    default_font = "Microsoft YaHei"

    def setup(self):
        """初始化所有教学场景共用的视觉状态。

        此方法由 Manim 生命周期自动调用。子类如需覆盖，应先执行
        ``super().setup()``，否则字幕等通用状态不会初始化。
        """
        super().setup()
        self.camera.background_color = BG
        Text.set_default(font=self.default_font)
        self.subtitle = None

    def play(self, *animations, **kwargs):
        """播放动画，并统一应用场景的速度倍率。

        Args:
            *animations: 传给 Manim ``Scene.play`` 的动画对象。
            **kwargs: Manim 支持的播放参数，例如 ``run_time``、
                ``rate_func`` 或 ``lag_ratio``。

        Notes:
            未提供 ``run_time`` 时以 Manim 默认的 1 秒为基础。最终时长为
            ``run_time * animation_slowdown``。例如倍率为 1.25 时，传入
            ``run_time=2`` 的动画实际播放 2.5 秒。
        """
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * self.animation_slowdown
        return super().play(*animations, **kwargs)

    def set_subtitle(self, content, duration=1.0):
        """显示一条非阻塞字幕，并在后续动画中自动淡出。

        Args:
            content: 字幕文本。
            duration: 字幕完全可见的时长，单位为秒，默认 1 秒。该时长
                不包含最后 0.25 秒的淡出过程。

        Notes:
            本方法只等待字幕的淡入动画，随后立即返回，不会使用
            ``self.wait(duration)`` 阻塞后续动画。字幕计时由 updater 驱动，
            因而只有场景继续播放动画或等待时，计时才会向前推进。

            如果上一条字幕还在画面中，会先停止它的自动计时，再将它
            替换成新字幕。
        """
        new_subtitle = Text(content, font_size=28, color=WHITE)
        new_subtitle.to_edge(DOWN, buff=0.28)
        backdrop = BackgroundRectangle(
            new_subtitle, color=BLACK, fill_opacity=0.72, buff=0.15
        )
        group = VGroup(backdrop, new_subtitle)
        if self.subtitle is None:
            self.play(FadeIn(group, shift=UP * 0.08), run_time=0.3)
        else:
            self.subtitle.clear_updaters()
            self.play(FadeOut(self.subtitle), FadeIn(group), run_time=0.25)
        self.subtitle = group

        elapsed = 0.0
        fade_duration = 0.25

        def auto_hide(mob, dt):
            """逐帧累计场景时间，并在到期后降低整个字幕组的透明度。"""
            nonlocal elapsed
            elapsed += dt
            if elapsed > duration:
                opacity = 1 - (elapsed - duration) / fade_duration
                mob.set_opacity(max(0, opacity))
            if elapsed >= duration + fade_duration:
                mob.clear_updaters()
                self.remove(mob)
                if self.subtitle is mob:
                    self.subtitle = None

        # updater 会与下一段动画同时运行，因此字幕计时不会阻塞时间线。
        group.add_updater(auto_hide)

    def clear_subtitle(self):
        """立即停止字幕自动计时，并用淡出动画清除当前字幕。

        当前没有字幕时不会执行任何操作。
        """
        if self.subtitle is not None:
            self.subtitle.clear_updaters()
            self.play(FadeOut(self.subtitle), run_time=0.2)
            self.subtitle = None

    def section_title(self, content):
        """创建左上角的章节标题和下划线。

        Args:
            content: 标题文本。

        Returns:
            包含标题与下划线的 ``VGroup``。本方法只创建对象，不会自动
            添加或播放，调用方可自行选择 ``FadeIn``、``Write`` 等动画。
        """
        title = Text(content, font_size=38, color=ACCENT)
        title.to_corner(UL, buff=0.42)
        rule = Line(LEFT, RIGHT, color=ACCENT, stroke_width=3)
        rule.set_width(min(title.width, 4.2)).next_to(title, DOWN, buff=0.12)
        return VGroup(title, rule)

    def pulse(
        self,
        *mobjects,
        color=ACCENT,
        duration=0.7,
        frequency=3.0,
        scale_factor=1.2,
    ):
        """让一个或多个对象以固定频率非阻塞闪动。

        Args:
            *mobjects: 要高亮的 Manim 对象。
            color: 闪动时覆盖在原对象上的强调色。
            duration: 闪动持续时间，单位为秒。
            frequency: 每秒闪动次数，单位为 Hz，默认每秒 3 次。
            scale_factor: 闪动最亮时的最大缩放倍数，默认放大到 1.08 倍。

        Notes:
            本方法不会调用 ``self.play`` 或 ``self.wait``，因此调用后会
            立即返回，后续动画可以和闪动同时进行。计时由 updater 驱动，
            只有场景继续播放动画或等待时，闪动时间才会向前推进。

            updater 直接修改原对象的尺寸和颜色，不创建覆盖副本，因此
            不会产生重影。每次闪动都以对象自身中心缩放，结束后恢复
            原始尺寸及填充、描边样式。
        """
        if not mobjects or duration <= 0:
            return
        if frequency <= 0:
            raise ValueError("frequency 必须大于 0")
        if scale_factor <= 0:
            raise ValueError("scale_factor 必须大于 0")

        highlight_color = ManimColor(color)

        def add_blink_updater(mobject):
            family = mobject.get_family()
            original_styles = [
                (
                    member.get_fill_color(),
                    member.get_fill_opacity(),
                    member.get_stroke_color(),
                    member.get_stroke_opacity(),
                )
                for member in family
            ]
            elapsed = 0.0
            current_scale = 1.0

            def blink(mob, dt):
                nonlocal elapsed, current_scale
                elapsed += dt

                strength = 0.5 - 0.5 * np.cos(TAU * frequency * elapsed)
                target_scale = 1 + (scale_factor - 1) * strength
                mob.scale(target_scale / current_scale, about_point=mob.get_center())
                current_scale = target_scale

                for member, style in zip(mob.get_family(), original_styles):
                    fill_color, fill_opacity, stroke_color, stroke_opacity = style
                    member.set_fill(
                        interpolate_color(fill_color, highlight_color, strength),
                        opacity=fill_opacity,
                    )
                    member.set_stroke(
                        interpolate_color(stroke_color, highlight_color, strength),
                        opacity=stroke_opacity,
                    )

                if elapsed >= duration:
                    mob.scale(1 / current_scale, about_point=mob.get_center())
                    for member, style in zip(mob.get_family(), original_styles):
                        fill_color, fill_opacity, stroke_color, stroke_opacity = style
                        member.set_fill(fill_color, opacity=fill_opacity)
                        member.set_stroke(stroke_color, opacity=stroke_opacity)
                    mob.remove_updater(blink)

            mobject.add_updater(blink)

        for mobject in mobjects:
            add_blink_updater(mobject)

    def clear_scene(self, *keep):
        """淡出场景中的全部顶层对象，可指定需要保留的对象。

        Args:
            *keep: 不参与清场的顶层 Mobject。判断依据是对象身份，而不是
                对象内容；应传入已经添加到场景中的原对象。

        清场结束后会重置字幕引用，通常用于两个教学章节之间的过渡。
        """
        keep_ids = {id(mob) for mob in keep}
        targets = [mob for mob in self.mobjects if id(mob) not in keep_ids]
        if targets:
            self.play(*[FadeOut(mob) for mob in targets], run_time=0.55)
        self.subtitle = None
