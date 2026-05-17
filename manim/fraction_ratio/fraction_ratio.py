"""
分数与比例 —— manim 教学动画
脚本依据：fraction_ratio.md

无需 LaTeX：所有分数用 Text + Line 拼接而成。

运行（在本目录下）：
    manim -pql fraction_ratio.py FractionRatio
高质量：
    manim -pqh fraction_ratio.py FractionRatio
"""

from manim import *


# ==========================================================
# 通用工具：自制分数（不依赖 LaTeX）
# ==========================================================
def make_frac(numer, denom, font_size=72, color=WHITE, bar_color=None):
    """用 Text + Line 拼一个分数。numer/denom 是字符串。返回 VGroup。"""
    if bar_color is None:
        bar_color = color
    n_text = Text(str(numer), font_size=font_size, color=color)
    d_text = Text(str(denom), font_size=font_size, color=color)
    width = max(n_text.width, d_text.width) * 1.25
    bar = Line(LEFT * width / 2, RIGHT * width / 2, color=bar_color, stroke_width=4)
    n_text.next_to(bar, UP, buff=0.12)
    d_text.next_to(bar, DOWN, buff=0.12)
    grp = VGroup(n_text, bar, d_text)
    # 暴露子部件方便外部访问
    grp.numer = n_text
    grp.bar = bar
    grp.denom = d_text
    return grp


def make_slices(center, radius=1.5, n=5, color=ORANGE):
    """把蛋糕在 center 处切成 n 份，从顶端开始顺时针。返回 VGroup。"""
    slices = VGroup()
    for i in range(n):
        start_angle = PI / 2 - (i + 1) * TAU / n
        sector = AnnularSector(
            inner_radius=0,
            outer_radius=radius,
            angle=TAU / n,
            start_angle=start_angle,
            stroke_color=WHITE,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.7,
        )
        sector.move_arc_center_to(center)
        slices.add(sector)
    return slices


# ==========================================================
# 主场景
# ==========================================================
class FractionRatio(Scene):
    def construct(self):
        Text.set_default(font="Microsoft YaHei")

        self.scene_title()
        self.scene_review_one_fifth()
        self.scene_six_fifth_trouble()
        self.scene_ratio_view()
        self.scene_apply_problem()
        self.scene_outro()

    # ---------- 1. 标题 ----------
    def scene_title(self):
        title = Text("分数 与 比例", font_size=80, color=YELLOW)
        sub = Text("换一种视角，看懂假分数", font_size=36).next_to(title, DOWN, buff=0.6)
        self.play(Write(title))
        self.play(FadeIn(sub, shift=UP))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(sub))

    # ---------- 2. 复习 1/5：蛋糕分 5 份取 1 份 ----------
    def scene_review_one_fifth(self):
        title = Text("回忆一下：1/5 是什么？", font_size=44, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        # 蛋糕居中
        center = LEFT * 3 + DOWN * 0.3
        slices = make_slices(center=center, radius=1.7, n=5, color=ORANGE)
        self.play(FadeIn(slices))

        step1 = Text("把蛋糕平均分成 5 份", font_size=30).shift(RIGHT * 2.6 + UP * 1.6)
        self.play(Write(step1))
        self.wait(0.4)

        # 取一份
        taken = slices[0]
        rest = VGroup(*slices[1:])
        step2 = Text("拿走其中 1 份", font_size=30).next_to(step1, DOWN, buff=0.4)
        self.play(Write(step2))
        self.play(taken.animate.set_fill(RED, opacity=0.95).set_stroke(YELLOW, width=4))
        self.play(taken.animate.shift(RIGHT * 5 + DOWN * 0.6))

        frac = make_frac("1", "5", font_size=84, color=RED).next_to(taken, DOWN, buff=0.4)
        self.play(Write(frac))
        self.wait(1.2)

        ok = Text("这一份就是蛋糕的 1/5", font_size=32, color=GREEN).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(ok, shift=UP))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [title, rest, taken, step1, step2, frac, ok]])

    # ---------- 3. 6/5 的困惑 ----------
    def scene_six_fifth_trouble(self):
        title = Text("那 6/5 呢？", font_size=44, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        # 居中重新画一个蛋糕
        center = LEFT * 3 + DOWN * 0.3
        slices = make_slices(center=center, radius=1.7, n=5, color=ORANGE)
        self.play(FadeIn(slices))

        statement = Text("“分成 5 份，拿走 6 份？”", font_size=32, color=YELLOW)
        statement.shift(RIGHT * 2.5 + UP * 1.5)
        self.play(Write(statement))
        self.wait(0.5)

        # 飞出 5 份到右边
        positions = [
            RIGHT * 3.0 + UP * 0.0,
            RIGHT * 4.6 + UP * 0.0,
            RIGHT * 3.0 + DOWN * 1.5,
            RIGHT * 4.6 + DOWN * 1.5,
            RIGHT * 3.8 + DOWN * 3.0,
        ]
        # 让位置避开顶部文字
        positions = [p + DOWN * 0.3 for p in positions]

        counter_label = Text("已拿：", font_size=30).shift(LEFT * 5 + DOWN * 2.8)
        counter = Integer(0, font_size=44, color=YELLOW).next_to(counter_label, RIGHT, buff=0.2)
        self.play(FadeIn(counter_label), FadeIn(counter))

        for i, s in enumerate(slices):
            self.play(
                s.animate.set_fill(RED, opacity=0.9).move_to(positions[i]).scale(0.7),
                counter.animate.set_value(i + 1),
                run_time=0.5,
            )

        self.wait(0.4)

        q = Text("第 6 份…在哪？", font_size=40, color=RED).move_to(LEFT * 3 + DOWN * 0.3)
        self.play(Write(q))
        self.wait(0.8)
        cross = Cross(stroke_color=RED, stroke_width=10).scale(1.5).move_to(q)
        self.play(Create(cross))
        self.wait(1.2)

        hint = Text("说明这种理解方式不够用！", font_size=32, color=ORANGE).to_edge(DOWN, buff=0.5)
        self.play(Write(hint))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [
            title, slices, statement, counter_label, counter, q, cross, hint
        ]])

    # ---------- 4. 比例视角：1/5 = 我 1 份 vs 你 5 份 ----------
    def scene_ratio_view(self):
        title = Text("换个角度：分数是一种“比例”", font_size=44, color=GREEN).to_edge(UP)
        self.play(Write(title))

        intro = Text("我有 1 份蛋糕，你有 5 份（一整块）", font_size=32).next_to(title, DOWN, buff=0.4)
        self.play(Write(intro))
        self.wait(0.5)

        # 左边：我（1 小份）
        me_label = Text("我", font_size=36, color=BLUE).shift(LEFT * 4.5 + UP * 0.5)
        my_piece = AnnularSector(
            inner_radius=0, outer_radius=0.7, angle=TAU / 5, start_angle=PI / 2 - TAU / 5,
            stroke_color=WHITE, stroke_width=3, fill_color=BLUE, fill_opacity=0.85,
        ).next_to(me_label, DOWN, buff=0.4)

        # 右边：你（完整 5 份）
        you_label = Text("你", font_size=36, color=ORANGE).shift(RIGHT * 2.5 + UP * 0.5)
        your_cake = make_slices(center=ORIGIN, radius=1.0, n=5, color=ORANGE)
        your_cake.next_to(you_label, DOWN, buff=0.4)

        self.play(
            FadeIn(me_label), FadeIn(my_piece),
            FadeIn(you_label), FadeIn(your_cake),
        )
        self.wait(0.6)

        # 显示比例 1:5 → 1/5
        ratio = Text("1 : 5", font_size=56, color=YELLOW).shift(DOWN * 2.7 + LEFT * 2.5)
        arrow = Arrow(start=ratio.get_right() + RIGHT * 0.2,
                      end=ratio.get_right() + RIGHT * 1.6, color=YELLOW, buff=0)
        frac = make_frac("1", "5", font_size=72, color=YELLOW).next_to(arrow, RIGHT, buff=0.3)

        self.play(Write(ratio))
        self.play(GrowArrow(arrow))
        self.play(Write(frac))
        self.wait(2)

        # 过渡到 6/5
        self.play(
            FadeOut(intro), FadeOut(ratio), FadeOut(arrow), FadeOut(frac),
        )
        intro2 = Text("如果我有 6 份，你有 5 份呢？", font_size=32).next_to(title, DOWN, buff=0.4)
        self.play(Write(intro2))
        self.wait(0.5)

        # 让"我"长出 6 个小份（比"你"还多一份）
        # 重新摆放：左侧用 6 个小扇形堆叠，呈一个完整 5 份蛋糕 + 多 1 份
        my_full_cake = make_slices(center=my_piece.get_center() + RIGHT * 0.0, radius=0.9, n=5, color=BLUE)
        # 把 my_piece 替换成完整蛋糕
        self.play(FadeOut(my_piece), FadeIn(my_full_cake))

        extra = AnnularSector(
            inner_radius=0, outer_radius=0.9, angle=TAU / 5, start_angle=PI / 2 - TAU / 5,
            stroke_color=WHITE, stroke_width=3, fill_color=BLUE, fill_opacity=0.95,
        )
        extra.move_arc_center_to(my_full_cake.get_center())
        # 把多出的那一份单独画在旁边（右上方）
        extra_target_pos = my_full_cake.get_center() + RIGHT * 1.5 + UP * 0.6
        extra.move_arc_center_to(extra_target_pos)
        extra.set_stroke(YELLOW, width=4)
        plus = Text("+1", font_size=32, color=YELLOW).next_to(extra, UP, buff=0.15)

        self.play(FadeIn(extra), Write(plus))
        self.wait(0.5)

        ratio2 = Text("6 : 5", font_size=56, color=YELLOW).shift(DOWN * 2.7 + LEFT * 2.5)
        arrow2 = Arrow(start=ratio2.get_right() + RIGHT * 0.2,
                       end=ratio2.get_right() + RIGHT * 1.6, color=YELLOW, buff=0)
        frac2 = make_frac("6", "5", font_size=72, color=YELLOW).next_to(arrow2, RIGHT, buff=0.3)

        self.play(Write(ratio2))
        self.play(GrowArrow(arrow2))
        self.play(Write(frac2))
        self.wait(1)

        conclusion = Text(
            "分数 = 两个量之间的比例关系",
            font_size=34, color=GREEN,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(conclusion))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in [
            title, intro2, me_label, my_full_cake, extra, plus,
            you_label, your_cake, ratio2, arrow2, frac2, conclusion,
        ]])

    # ---------- 5. 应用题：72 人占 3/100，求全校人数 ----------
    def scene_apply_problem(self):
        title = Text("来做一道题", font_size=44, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        # 题目
        prob1 = Text("学校数学考试满分的学生有 72 人，", font_size=30)
        prob2 = Text("占全校人数的 3/100。", font_size=30)
        prob3 = Text("全校共有多少人？", font_size=30, color=YELLOW)
        problem = VGroup(prob1, prob2, prob3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        problem.next_to(title, DOWN, buff=0.5)
        self.play(Write(prob1))
        self.play(Write(prob2))
        self.play(Write(prob3))
        self.wait(1.5)

        # 移到左上角，腾出空间
        self.play(problem.animate.scale(0.7).to_edge(LEFT, buff=0.5).shift(UP * 1.8))
        self.wait(0.3)

        # 第一步：把"占 3/100"翻译成比例
        step1 = Text("第 1 步：转成比例", font_size=30, color=BLUE).shift(UP * 0.8 + RIGHT * 1.0)
        self.play(Write(step1))

        ratio_line = Text("满分人数 : 全校人数 = 3 : 100", font_size=32).next_to(step1, DOWN, buff=0.3)
        self.play(Write(ratio_line))
        self.wait(1.2)

        # 第二步：写成等式
        step2 = Text("第 2 步：写成分数等式", font_size=30, color=BLUE).next_to(ratio_line, DOWN, buff=0.5)
        self.play(Write(step2))

        # 等式： 72/x = 3/100
        left_frac = make_frac("72", "全校人数", font_size=44, color=WHITE)
        eq_sign = Text("=", font_size=52).next_to(left_frac, RIGHT, buff=0.4)
        right_frac = make_frac("3", "100", font_size=44, color=WHITE).next_to(eq_sign, RIGHT, buff=0.4)
        equation = VGroup(left_frac, eq_sign, right_frac)
        equation.next_to(step2, DOWN, buff=0.4)
        self.play(Write(equation))
        self.wait(1.5)

        # 第三步：交叉相乘
        step3 = Text("第 3 步：交叉相乘", font_size=30, color=BLUE).to_edge(DOWN, buff=2.4).shift(LEFT * 2.0)
        self.play(Write(step3))

        # 用两条彩色线表示交叉
        cross1 = Line(
            left_frac.numer.get_center(),
            right_frac.denom.get_center(),
            color=RED, stroke_width=4,
        )
        cross2 = Line(
            left_frac.denom.get_center(),
            right_frac.numer.get_center(),
            color=GREEN, stroke_width=4,
        )
        self.play(Create(cross1), Create(cross2))
        self.wait(0.6)

        # 写出 72 * 100 = 3 * 全校人数
        cross_eq = Text("72 × 100 = 3 × 全校人数", font_size=36, color=YELLOW)
        cross_eq.to_edge(DOWN, buff=1.4)
        self.play(Write(cross_eq))
        self.wait(1.5)

        # 第四步：求解
        step4 = Text("第 4 步：解出来", font_size=30, color=BLUE).next_to(step3, RIGHT, buff=2.5)
        self.play(Write(step4))

        solve_eq = Text("全校人数 = 72 × 100 ÷ 3 = 2400", font_size=36, color=GREEN)
        solve_eq.to_edge(DOWN, buff=0.5)
        self.play(Write(solve_eq))
        self.wait(0.6)

        # 高亮答案
        ans_box = SurroundingRectangle(solve_eq[-4:], color=YELLOW, buff=0.15)
        self.play(Create(ans_box))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in [
            title, problem, step1, ratio_line, step2, equation,
            cross1, cross2, cross_eq, step3, step4, solve_eq, ans_box,
        ]])

    # ---------- 6. 收尾 ----------
    def scene_outro(self):
        line1 = Text("分数 = 比例", font_size=72, color=YELLOW)
        line2 = Text("比例问题 → 分数等式 → 交叉相乘", font_size=36, color=GREEN)
        line2.next_to(line1, DOWN, buff=0.6)

        self.play(Write(line1))
        self.play(FadeIn(line2, shift=UP))
        self.wait(2.5)

        thx = Text("下次再见！", font_size=44).to_edge(DOWN, buff=0.8)
        self.play(Write(thx))
        self.wait(2)
        self.play(FadeOut(line1), FadeOut(line2), FadeOut(thx))
