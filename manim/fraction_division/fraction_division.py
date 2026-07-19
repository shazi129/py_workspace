"""分数的除法教学动画。

运行：python -m manim -pql fraction_division.py FractionDivision
"""

from manim import *
import numpy as np


BG = "#10151C"
ACCENT = "#F5C451"
BLUE_ACCENT = "#4DB6E7"
GREEN_ACCENT = "#69D39B"
PINK_ACCENT = "#F08080"


class FractionDivision(Scene):
    def construct(self):
        self.camera.background_color = BG
        Text.set_default(font="Microsoft YaHei")
        self.subtitle = None

        self.cover()
        self.review_division()
        self.fraction_divided_by_integer()
        self.integer_divided_by_fraction()
        self.algebraic_derivation()

    # ---------- 通用组件 ----------
    def set_subtitle(self, content, wait=0.35):
        new_subtitle = Text(content, font_size=28, color=WHITE)
        new_subtitle.to_edge(DOWN, buff=0.28)
        backdrop = BackgroundRectangle(
            new_subtitle, color=BLACK, fill_opacity=0.72, buff=0.15
        )
        group = VGroup(backdrop, new_subtitle)
        if self.subtitle is None:
            self.play(FadeIn(group, shift=UP * 0.08), run_time=0.3)
        else:
            self.play(FadeOut(self.subtitle), FadeIn(group), run_time=0.25)
        self.subtitle = group
        self.wait(wait)

    def clear_subtitle(self):
        if self.subtitle is not None:
            self.play(FadeOut(self.subtitle), run_time=0.2)
            self.subtitle = None

    def section_title(self, content):
        title = Text(content, font_size=38, color=ACCENT)
        title.to_corner(UL, buff=0.42)
        rule = Line(LEFT, RIGHT, color=ACCENT, stroke_width=3)
        rule.set_width(min(title.width, 4.2)).next_to(title, DOWN, buff=0.12)
        return VGroup(title, rule)

    def pulse(self, *mobjects, color=ACCENT):
        self.play(
            *[Indicate(mob, color=color, scale_factor=1.13) for mob in mobjects],
            run_time=0.7,
        )

    def clear_scene(self, *keep):
        keep_ids = {id(mob) for mob in keep}
        targets = [mob for mob in self.mobjects if id(mob) not in keep_ids]
        if targets:
            self.play(*[FadeOut(mob) for mob in targets], run_time=0.55)
        self.subtitle = None

    # ---------- 1. 封面 ----------
    def cover(self):
        title = Text("分数的除法", font_size=76, color=ACCENT)
        underline = Line(LEFT * 2.5, RIGHT * 2.5, color=BLUE_ACCENT)
        underline.next_to(title, DOWN, buff=0.3)
        group = VGroup(title, underline)

        self.play(FadeIn(group, shift=RIGHT * 1.2), run_time=1.2)
        self.wait(3)
        self.play(FadeOut(group, shift=RIGHT * 1.2), run_time=1.2)

    # ---------- 2. 回顾除法 ----------
    def review_division(self):
        title = Text("回顾：什么是除法", font_size=48, color=ACCENT)
        self.play(Write(title))
        self.set_subtitle("我们先来回顾一下什么是除法")
        target = title.copy().scale(0.78).to_corner(UL, buff=0.42)
        self.play(Transform(title, target))

        six, divide_three, equals_two = MathTex("6", r"\div 3", "=2", font_size=70)
        equation = VGroup(six, divide_three, equals_two).arrange(RIGHT, buff=0.18)
        equation.to_edge(UP, buff=0.5).shift(RIGHT * 2.4)
        self.play(Write(equation))
        self.set_subtitle("为什么六除以三等于二？")

        dots = VGroup(*[
            Dot(radius=0.25, color=BLUE_ACCENT).move_to(
                np.array([-2.2 + (i % 3) * 1.25, 0.7 - (i // 3) * 1.15, 0])
            ) for i in range(6)
        ])
        self.pulse(six)
        self.play(LaggedStart(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.1))

        self.pulse(divide_three)
        columns = VGroup(*[
            SurroundingRectangle(VGroup(dots[i], dots[i + 3]), buff=0.2, color=ACCENT)
            for i in range(3)
        ])
        self.play(LaggedStart(*[Create(box) for box in columns], lag_ratio=0.18))
        self.pulse(equals_two)
        sample = VGroup(dots[0], dots[3]).copy()
        sample_target = sample.copy().arrange(DOWN, buff=0.55).move_to(RIGHT * 3.4 + UP * 0.25)
        self.add(sample)
        self.play(Transform(sample, sample_target))
        brace = Brace(sample, RIGHT, color=GREEN_ACCENT)
        count = MathTex("2", font_size=52, color=GREEN_ACCENT).next_to(brace, RIGHT)
        self.play(GrowFromCenter(brace), Write(count))
        self.set_subtitle("六平均分成三份，每份有两个")

        self.play(FadeOut(sample), FadeOut(brace), FadeOut(count), FadeOut(columns))
        self.pulse(divide_three)
        rows = VGroup(*[
            SurroundingRectangle(VGroup(*dots[i * 3:(i + 1) * 3]), buff=0.2, color=PINK_ACCENT)
            for i in range(2)
        ])
        self.play(Create(rows[0]), Create(rows[1]))
        self.pulse(equals_two)
        row_copies = rows.copy()
        self.play(row_copies.animate.scale(0.72).move_to(RIGHT * 3.35 + DOWN * 0.65))
        brace2 = Brace(row_copies, RIGHT, color=GREEN_ACCENT)
        count2 = MathTex("2", font_size=52, color=GREEN_ACCENT).next_to(brace2, RIGHT)
        self.play(GrowFromCenter(brace2), Write(count2))
        self.set_subtitle("也可以理解为：六里面有两个三")
        self.wait(1)
        self.clear_subtitle()
        self.clear_scene()

    # ---------- 3. 分数除以整数 ----------
    def fraction_divided_by_integer(self):
        title = self.section_title("分数除以整数")
        self.play(FadeIn(title))

        lhs = MathTex(
            r"\frac{4}{5}", r"\div", "2", "=",
            substrings_to_isolate=["4", "5"],
            font_size=64,
        )
        numerator = lhs.get_part_by_tex("4")
        denominator = lhs.get_part_by_tex("5")
        division_term = VGroup(lhs.get_part_by_tex(r"\div"), lhs.get_part_by_tex("2"))
        question = MathTex("?", font_size=64, color=ACCENT)
        equation = VGroup(lhs, question).arrange(RIGHT, buff=0.15)
        equation.to_corner(UR, buff=0.55)
        self.play(Write(equation))
        self.pulse(question)
        self.set_subtitle("五分之四除以二等于多少呢？")

        grid = VGroup()
        cells = VGroup()
        left, bottom, width, height = -4.8, -1.25, 7.0, 2.2
        for col in range(5):
            cell = Rectangle(width=width / 5, height=height, stroke_color=WHITE)
            cell.move_to([left + width * (col + 0.5) / 5, bottom + height / 2, 0])
            cells.add(cell)
        grid.add(cells)

        # 1. 分母 5：先把整体平均分成 5 份。
        self.play(
            Indicate(denominator, color=ACCENT, scale_factor=1.13),
            LaggedStart(*[Create(cell) for cell in cells], lag_ratio=0.1),
            run_time=1.0,
        )
        self.set_subtitle("分母五表示把整体平均分成五份")

        # 2. 分子 4：再标出其中 4 份，并显示四分之五。
        frac_label = MathTex(r"\frac{4}{5}", font_size=48, color=BLUE_ACCENT).next_to(cells, DOWN)
        self.play(
            Indicate(numerator, color=ACCENT, scale_factor=1.13),
            *[
                cells[col].animate.set_fill(BLUE_ACCENT, opacity=0.62)
                for col in range(4)
            ],
            Write(frac_label),
            run_time=1.0,
        )
        self.set_subtitle("这块阴影表示五分之四")

        # 3. 除以 2：用横线把每一份再平均分成上下两份。
        midline = Line([left, bottom + height / 2, 0], [left + width, bottom + height / 2, 0], color=ACCENT)
        self.play(
            Indicate(division_term, color=ACCENT, scale_factor=1.13),
            Create(midline),
            run_time=1.0,
        )
        self.set_subtitle("除以二，就是再把它平均分成上下两份")

        # 4. 用斜线标出其中一份，同时给出结果。
        selected = VGroup()
        hatch_slope = 2.0
        hatch_spacing = 0.3
        for col in range(4):
            x0 = left + width * col / 5
            x1 = left + width * (col + 1) / 5
            y0 = bottom + height / 2
            y1 = bottom + height
            # y = y0 + hatch_slope * (x - base_x)。分别与小格的
            # 左、右、下、上边求交点，确保斜线不会伸出格子。
            for base_x in np.arange(
                x0 - (y1 - y0) / hatch_slope,
                x1 + hatch_spacing,
                hatch_spacing,
            ):
                start_x = max(x0, base_x)
                end_x = min(x1, base_x + (y1 - y0) / hatch_slope)
                if end_x - start_x > 1e-6:
                    start_y = y0 + hatch_slope * (start_x - base_x)
                    end_y = y0 + hatch_slope * (end_x - base_x)
                    selected.add(Line(
                        [start_x, start_y, 0],
                        [end_x, end_y, 0],
                        color=ACCENT,
                        stroke_width=2,
                    ))
        answer = MathTex(r"\frac{4}{10}", font_size=60, color=GREEN_ACCENT).move_to(question)
        answer_label = MathTex(r"\frac{4}{10}", font_size=45, color=GREEN_ACCENT).next_to(cells, DOWN)
        self.play(Create(selected), ReplacementTransform(question, answer), Transform(frac_label, answer_label))
        self.set_subtitle("把五分之四平均分成两份，每份是十分之四")

        rule_calc = MathTex(r"5\times2=10", font_size=56, color=ACCENT).move_to(RIGHT * 3 + DOWN * 0.7)
        self.pulse(lhs, answer)
        self.play(FadeIn(rule_calc, shift=UP * 0.2))
        self.set_subtitle("分数除以一个数，可以把分母乘以这个数")
        self.play(FadeOut(rule_calc))

        full_equation = MathTex(
            r"\frac{4}{5}\div2=\frac{4}{10}=\frac{2}{5}",
            font_size=58,
        ).move_to(equation)
        self.play(ReplacementTransform(VGroup(lhs, answer), full_equation))
        calc2 = MathTex(r"4\div2=2", font_size=56, color=ACCENT).move_to(RIGHT * 3 + DOWN * 0.7)
        self.pulse(full_equation)
        self.play(FadeIn(calc2, shift=UP * 0.2))
        self.set_subtitle("能整除时，也可以把分子除以这个数")
        self.wait(1)
        self.clear_subtitle()
        self.clear_scene()

    # ---------- 4. 整数除以分数 ----------
    def integer_divided_by_fraction(self):
        title = self.section_title("整数除以分数")
        self.play(FadeIn(title))
        lhs = MathTex(r"3\div\frac{3}{4}=", font_size=62)
        question = MathTex("?", font_size=62, color=ACCENT)
        equation = VGroup(lhs, question).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.55)
        self.play(Write(equation))
        self.pulse(question)
        self.set_subtitle("三除以四分之三等于多少呢？")

        circles = VGroup(*[
            Circle(radius=0.82, color=WHITE, fill_color=BLUE_ACCENT, fill_opacity=0.55)
            for _ in range(3)
        ]).arrange(RIGHT, buff=0.65).move_to(LEFT * 1.6 + DOWN * 0.25)
        self.pulse(lhs[0])
        self.play(LaggedStart(*[GrowFromCenter(c) for c in circles], lag_ratio=0.15))
        self.set_subtitle("这是三个完整的单位")
        self.pulse(lhs[1:])
        self.set_subtitle("现在要计算里面有多少个四分之三")

        divisions = VGroup()
        quarters = []
        for circle in circles:
            center = circle.get_center()
            divisions.add(Line(center + LEFT * 0.82, center + RIGHT * 0.82, color=WHITE))
            divisions.add(Line(center + DOWN * 0.82, center + UP * 0.82, color=WHITE))
            for k in range(4):
                sector = Sector(
                    radius=0.82, angle=PI / 2, start_angle=k * PI / 2,
                    fill_color=GREEN_ACCENT, fill_opacity=0.75, stroke_color=WHITE,
                ).move_arc_center_to(center)
                quarters.append(sector)
        self.play(Create(divisions))

        groups = VGroup()
        targets = [LEFT * 3.6, LEFT * 1.2, RIGHT * 1.2, RIGHT * 3.6]
        for idx in range(4):
            source = VGroup(*[
                quarters[idx * 3 + j].copy() for j in range(3)
            ])
            target_center = targets[idx] + DOWN * 2.15
            target = VGroup(*[
                Sector(
                    radius=0.65,
                    angle=PI / 2,
                    start_angle=j * PI / 2,
                    fill_color=GREEN_ACCENT,
                    fill_opacity=0.85,
                    stroke_color=WHITE,
                    stroke_width=2,
                ).move_arc_center_to(target_center)
                for j in range(3)
            ])
            self.add(source)
            self.play(Transform(source, target), run_time=0.55)
            groups.add(source)
        brace = Brace(groups, DOWN, color=ACCENT)
        four = MathTex("4", font_size=52, color=ACCENT).next_to(brace, DOWN)
        answer = MathTex("4", font_size=62, color=GREEN_ACCENT).move_to(question)
        self.play(GrowFromCenter(brace), Write(four), ReplacementTransform(question, answer))
        self.set_subtitle("三个单位中一共有四个四分之三，答案是四")

        self.play(FadeOut(groups), FadeOut(brace), FadeOut(four), FadeOut(divisions))
        self.set_subtitle("再来总结一下规律")
        self.play(Create(divisions))
        derivation = MathTex(r"3\times4\div3", font_size=54, color=ACCENT)
        derivation.next_to(equation, DOWN, buff=0.55)
        self.play(Write(derivation))
        # 圆和分割线必须一起参与缩放，否则 Indicate 动画中会发生错位。
        self.pulse(VGroup(circles, divisions), color=BLUE_ACCENT)
        self.pulse(derivation, color=GREEN_ACCENT)
        self.set_subtitle("三个单位各分成四份，再每三份组成一组")

        final_eq = MathTex(
            r"3\div\frac{3}{4}=4=3\times4\div3=3\times\frac{4}{3}",
            font_size=52,
        ).move_to(DOWN * 2.35)
        self.play(FadeOut(derivation), FadeOut(equation), Write(final_eq))
        self.set_subtitle("继续推导：除以四分之三，就是乘以它的倒数三分之四")
        box = SurroundingRectangle(final_eq[-4:], color=ACCENT, buff=0.15)
        self.play(Create(box))
        self.set_subtitle("除以一个分数，等于乘以这个分数的倒数")
        self.wait(1)
        self.clear_subtitle()
        self.clear_scene()

    # ---------- 5. 代数推导 ----------
    def algebraic_derivation(self):
        title = self.section_title("代数推导")
        self.play(FadeIn(title))

        rules = [
            ("规律 1", r"\frac{b}{a}\div c=b\div a\div c=b\div(a\times c)=\frac{b}{a\times c}",
             "分数除以一个数，可以把分母乘以这个数"),
            ("规律 2", r"\frac{b}{a}\div c=b\div a\div c=b\div c\div a=\frac{b\div c}{a}",
             "能整除时，也可以把分子除以这个数"),
            ("规律 3", r"a\div\frac{c}{b}=a\div(c\div b)=a\div c\times b=a\times\frac{b}{c}",
             "一个数除以一个分数，等于乘以这个分数的倒数"),
        ]
        current = None
        for name, formula, subtitle in rules:
            label = Text(name, font_size=32, color=ACCENT)
            math = MathTex(formula, font_size=43)
            group = VGroup(label, math).arrange(DOWN, buff=0.35).move_to(DOWN * 0.15)
            if current is None:
                self.play(Write(group))
            else:
                self.play(ReplacementTransform(current, group))
            current = group
            self.set_subtitle(subtitle)
            self.wait(1)

        bridge = MathTex(
            r"\frac{b}{a}\div c", "=",
            r"\frac{b}{a\times c}", "=",
            r"\frac{b}{a}\times\frac{1}{c}",
            font_size=52,
        ).move_to(DOWN * 0.05)
        self.play(ReplacementTransform(current, bridge))
        self.set_subtitle("你发现了吗？规律一和规律三也可以相互推导")

        rule1_box = SurroundingRectangle(bridge[2], color=PINK_ACCENT, buff=0.16)
        rule3_box = SurroundingRectangle(bridge[4], color=PINK_ACCENT, buff=0.16)
        rule1_label = Text("规律 1", font_size=26, color=PINK_ACCENT).next_to(
            rule1_box, UP, buff=0.16
        )
        rule3_label = Text("规律 3", font_size=26, color=PINK_ACCENT).next_to(
            rule3_box, UP, buff=0.16
        )
        annotations = VGroup(rule1_box, rule3_box, rule1_label, rule3_label)
        self.play(
            Create(rule1_box), FadeIn(rule1_label, shift=DOWN * 0.08),
            Create(rule3_box), FadeIn(rule3_label, shift=DOWN * 0.08),
        )

        closing = Text("聪明的你，也可以继续推导其他规律", font_size=40, color=GREEN_ACCENT)
        closing.next_to(bridge, DOWN, buff=0.75)
        self.play(FadeIn(closing, shift=UP * 0.2))
        self.set_subtitle("聪明的你，也可以推导其他规律哦")
        self.wait(2)
        self.clear_subtitle()
        self.play(FadeOut(title), FadeOut(bridge), FadeOut(annotations), FadeOut(closing))


class Cover(Scene):
    """仅渲染封面，便于快速预览。"""

    def construct(self):
        self.camera.background_color = BG
        Text.set_default(font="Microsoft YaHei")
        title = Text("分数的除法", font_size=76, color=ACCENT)
        self.play(FadeIn(title, shift=RIGHT))
        self.wait(3)
        self.play(FadeOut(title, shift=RIGHT))
