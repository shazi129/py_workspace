"""
分数与比例 —— manim 教学动画
脚本依据：fraction_ratio.md

已启用 LaTeX：数学公式使用 MathTex 排版，中文说明继续使用 Text。

运行（在本目录下）：
    manim -pql fraction_ratio.py FractionRatio
高质量：
    manim -pqh fraction_ratio.py FractionRatio
"""

from manim import *
import numpy as np


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
        # self.scene_ratio_view()
        # self.scene_apply_problem()
        # self.scene_baseline_comparison()
        # self.scene_money_problem()
        # self.scene_outro()

    # ---------- 1. 标题 ----------
    def scene_title(self):
        title = Text("分数量和率", font_size=72, color=YELLOW)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))

    # ---------- 2. 复习 1/5：蛋糕分 5 份取 1 份 ----------
    def scene_review_one_fifth(self):
        # 标题：中文 + LaTeX 分数 横排拼接
        title_text = Text("什么是分数的量？", font_size=40, color=YELLOW)
        title_text.to_edge(UP)
        self.play(Write(title_text))

        # 把蛋糕平均分成 5 份
        center = ORIGIN + DOWN * 0.3
        slices = make_slices(center=center, radius=1.7, n=5, color=ORANGE)
        caption = Text("把一个蛋糕平均分成 5 份", font_size=32).next_to(slices, DOWN, buff=0.5)
        self.play(FadeIn(slices), Write(caption))
        self.wait(0.5)

        # 高亮其中一份（顶端那片）并闪烁
        target = slices[0]
        # 先把目标变红 + 黄色描边
        self.play(
            target.animate.set_fill(RED, opacity=0.95).set_stroke(YELLOW, width=5),
            run_time=0.6,
        )
        # 闪烁 3 次
        for _ in range(3):
            self.play(target.animate.set_stroke(WHITE, width=2), run_time=0.25)
            self.play(target.animate.set_stroke(YELLOW, width=6), run_time=0.25)

        self.wait(0.3)

        # 在高亮那份蛋糕旁标明 1/5
        frac_label = MathTex(r"\frac{1}{5}", font_size=84, color=WHITE)
        # 放到蛋糕右侧偏下，避免与顶部标题重叠
        frac_label.next_to(slices, RIGHT, buff=1.0).shift(UP * 0.2)
        arrow = Arrow(
            start=frac_label.get_left(),
            end=target.get_center() + UP * 0.3 + RIGHT * 0.1,
            color=WHITE, buff=0.15, stroke_width=4,
        )
        self.play(Write(frac_label), GrowArrow(arrow))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in [title, slices, caption, frac_label, arrow]])


    # ---------- 3. 6/5 的困惑 ----------
    def scene_six_fifth_trouble(self):
        # 标题：那 6/5 呢？
        title_a = Text("那 ", font_size=40, color=YELLOW)
        title_frac = MathTex(r"\frac{6}{5}", font_size=56, color=YELLOW)
        title_b = Text(" 呢？", font_size=40, color=YELLOW)
        title = VGroup(title_a, title_frac, title_b).arrange(RIGHT, buff=0.15)
        title.to_edge(UP)
        self.play(Write(title))

        # 左侧：一个蛋糕分成 5 份
        left_center = LEFT * 3.5 + DOWN * 0.3
        slices = make_slices(center=left_center, radius=1.5, n=5, color=ORANGE)
        caption = Text("一个蛋糕分成 5 份", font_size=28).next_to(slices, DOWN, buff=0.4)
        self.play(FadeIn(slices), Write(caption))
        self.wait(0.5)

        # 右侧网格：6 个目标位置（2 列 × 3 行）
        right_anchor = RIGHT * 2.8 + UP * 1.3
        col_gap = 1.4
        row_gap = 1.4
        targets = [
            right_anchor + LEFT * col_gap / 2 + DOWN * 0 * row_gap,
            right_anchor + RIGHT * col_gap / 2 + DOWN * 0 * row_gap,
            right_anchor + LEFT * col_gap / 2 + DOWN * 1 * row_gap,
            right_anchor + RIGHT * col_gap / 2 + DOWN * 1 * row_gap,
            right_anchor + LEFT * col_gap / 2 + DOWN * 2 * row_gap,
            right_anchor + RIGHT * col_gap / 2 + DOWN * 2 * row_gap,
        ]

        # 计数器
        counter_label = Text("已复制：", font_size=28).to_edge(DOWN, buff=0.6).shift(LEFT * 4)
        counter = Text("0", font_size=40, color=YELLOW).next_to(counter_label, RIGHT, buff=0.2)
        self.play(FadeIn(counter_label), FadeIn(counter))

        # 复制源：顶端那一份
        source_piece = slices[0]
        copies = VGroup()

        for i in range(6):
            # 复制一份，先叠加在源头上，然后飞到右侧目标位置并缩小
            clone = source_piece.copy()
            clone.set_fill(RED, opacity=0.9).set_stroke(YELLOW, width=3)
            self.add(clone)

            # 同时高亮一下源头作为视觉提示
            new_counter = Text(str(i + 1), font_size=40, color=YELLOW).move_to(counter)
            self.play(
                clone.animate.scale(0.6).move_to(targets[i]),
                Indicate(source_piece, color=YELLOW, scale_factor=1.15),
                Transform(counter, new_counter),
                run_time=0.55,
            )
            copies.add(clone)

        self.wait(0.5)

        # 在右侧 6 小份旁标明 6/5
        frac_label = MathTex(r"\frac{6}{5}", font_size=96, color=RED)
        # 放到 6 份的右侧
        frac_label.next_to(copies, RIGHT, buff=0.6)
        # 如果空间不够（已经贴近右边界），就改到下方
        if frac_label.get_right()[0] > 6.5:
            frac_label.next_to(copies, DOWN, buff=0.4)

        brace = Brace(copies, LEFT, color=RED)
        self.play(GrowFromCenter(brace))
        self.play(Write(frac_label))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [
            title, slices, caption, copies, brace, frac_label,
            counter_label, counter,
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
        ratio = MathTex(r"1:5", font_size=62, color=YELLOW).shift(DOWN * 2.7 + LEFT * 2.5)
        arrow = Arrow(start=ratio.get_right() + RIGHT * 0.2,
                      end=ratio.get_right() + RIGHT * 1.6, color=YELLOW, buff=0)
        frac = MathTex(r"\frac{1}{5}", font_size=76, color=YELLOW).next_to(arrow, RIGHT, buff=0.3)

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
        plus = MathTex(r"+1", font_size=36, color=YELLOW).next_to(extra, UP, buff=0.15)

        self.play(FadeIn(extra), Write(plus))
        self.wait(0.5)

        ratio2 = MathTex(r"6:5", font_size=62, color=YELLOW).shift(DOWN * 2.7 + LEFT * 2.5)
        arrow2 = Arrow(start=ratio2.get_right() + RIGHT * 0.2,
                       end=ratio2.get_right() + RIGHT * 1.6, color=YELLOW, buff=0)
        frac2 = MathTex(r"\frac{6}{5}", font_size=76, color=YELLOW).next_to(arrow2, RIGHT, buff=0.3)

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

        # 等式：设 x = 全校人数，使用 LaTeX 展示比例等式
        x_note = Text("设 x = 全校人数", font_size=28, color=GREEN).next_to(step2, DOWN, buff=0.35)
        left_frac = MathTex(r"\frac{72}{x}", font_size=58, color=WHITE)
        eq_sign = MathTex(r"=", font_size=58, color=WHITE).next_to(left_frac, RIGHT, buff=0.45)
        right_frac = MathTex(r"\frac{3}{100}", font_size=58, color=WHITE).next_to(eq_sign, RIGHT, buff=0.45)
        equation = VGroup(left_frac, eq_sign, right_frac).next_to(x_note, DOWN, buff=0.35)
        self.play(Write(x_note))
        self.play(Write(equation))
        self.wait(1.5)

        # 第三步：交叉相乘，只在分数等式上画交叉线
        step3 = Text("第 3 步：交叉相乘", font_size=30, color=BLUE).to_edge(DOWN, buff=0.65)
        self.play(Write(step3))

        cross1 = Line(
            left_frac.get_top() + DOWN * 0.12,
            right_frac.get_bottom() + UP * 0.12,
            color=RED, stroke_width=4,
        )
        cross2 = Line(
            left_frac.get_bottom() + UP * 0.12,
            right_frac.get_top() + DOWN * 0.12,
            color=GREEN, stroke_width=4,
        )
        self.play(Create(cross1), Create(cross2))
        self.wait(1.2)

        # 进入单独的计算页，避免等式、交叉线和计算过程互相重叠
        self.play(
            FadeOut(step1), FadeOut(ratio_line), FadeOut(step2), FadeOut(x_note), FadeOut(equation),
            FadeOut(cross1), FadeOut(cross2), FadeOut(step3),
        )

        calc_title = Text("根据交叉相乘", font_size=34, color=BLUE).shift(UP * 1.0)
        cross_eq = MathTex(r"72 \times 100 = 3x", font_size=58, color=YELLOW)
        cross_eq.next_to(calc_title, DOWN, buff=0.45)
        self.play(Write(calc_title))
        self.play(Write(cross_eq))
        self.wait(1.2)

        step4 = Text("第 4 步：解出来", font_size=32, color=BLUE).next_to(cross_eq, DOWN, buff=0.55)
        solve_eq = MathTex(r"x = \frac{72 \times 100}{3} = 2400", font_size=54, color=GREEN)
        solve_eq.next_to(step4, DOWN, buff=0.35)
        result_note = Text("所以全校人数是 2400 人", font_size=34, color=GREEN).next_to(solve_eq, DOWN, buff=0.35)
        self.play(Write(step4))
        self.play(Write(solve_eq))
        self.play(FadeIn(result_note, shift=UP))
        self.wait(0.6)

        ans_box = SurroundingRectangle(result_note, color=YELLOW, buff=0.15)
        self.play(Create(ans_box))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in [
            title, problem, calc_title, cross_eq, step4, solve_eq, result_note, ans_box,
        ]])

    # ---------- 6. 基准：比较依赖参照对象 ----------
    def scene_baseline_comparison(self):
        title = Text("比较时，一定要看“基准”", font_size=44, color=YELLOW).to_edge(UP)
        concept = Text("有比较，才有高矮、多少；基准不同，结论可能不同。", font_size=30)
        concept.next_to(title, DOWN, buff=0.4)
        self.play(Write(title))
        self.play(FadeIn(concept, shift=UP))

        floor = Line(LEFT * 5.5 + DOWN * 2.5, RIGHT * 5.5 + DOWN * 2.5, color=GRAY)
        self.play(Create(floor))

        def make_height_bar(name, height_text, height_value, color, x_pos):
            bottom = np.array([x_pos, -2.5, 0])
            top = bottom + UP * (height_value * 2.0)
            bar = Line(bottom, top, color=color, stroke_width=10)
            dot = Dot(top, color=color)
            name_label = Text(name, font_size=28, color=color).next_to(bar, DOWN, buff=0.25)
            height_label = Text(height_text, font_size=24).next_to(bar, UP, buff=0.15)
            return VGroup(bar, dot, name_label, height_label)

        lisi = make_height_bar("李四", "1.6m", 1.6, BLUE, -3.2)
        zhangsan = make_height_bar("张三", "1.7m", 1.7, GREEN, 0)
        wangwu = make_height_bar("王五", "1.8m", 1.8, RED, 3.2)

        self.play(FadeIn(lisi), FadeIn(zhangsan))
        base1 = SurroundingRectangle(lisi, color=BLUE, buff=0.15)
        compare1 = Text("以李四为基准：张三是高的", font_size=34, color=GREEN).to_edge(DOWN, buff=0.65)
        self.play(Create(base1), Write(compare1))
        self.wait(2)

        self.play(FadeIn(wangwu))
        base2 = SurroundingRectangle(wangwu, color=RED, buff=0.15)
        compare2 = Text("以王五为基准：张三又变矮了", font_size=34, color=RED).to_edge(DOWN, buff=0.65)
        self.play(ReplacementTransform(base1, base2), Transform(compare1, compare2))
        self.wait(2.2)

        summary = Text("理解分数，也要先找清楚比较的基准。", font_size=34, color=YELLOW)
        summary.next_to(concept, DOWN, buff=0.35)
        self.play(Write(summary))
        self.wait(2)

        self.play(*[FadeOut(m) for m in [
            title, concept, floor, lisi, zhangsan, wangwu, base2, compare1, summary,
        ]])

    # ---------- 7. 应用题：李四比张三多 1/4 ----------
    def scene_money_problem(self):
        title = Text("再看一道题", font_size=44, color=YELLOW).to_edge(UP)
        self.play(Write(title))

        problem = Text("张三有 8 元，李四比张三多 1/4，李四有多少钱？", font_size=30)
        problem.next_to(title, DOWN, buff=0.45)
        self.play(Write(problem))
        self.wait(1)

        zhang_label = Text("张三：8 元", font_size=30, color=BLUE).shift(LEFT * 3.8 + UP * 0.6)
        zhang_bar = Rectangle(width=4.0, height=0.55, color=BLUE, fill_color=BLUE, fill_opacity=0.65)
        zhang_bar.next_to(zhang_label, DOWN, buff=0.25).align_to(zhang_label, LEFT)

        self.play(FadeIn(zhang_label), GrowFromEdge(zhang_bar, LEFT))

        ratio_label = Text("多的钱 : 张三的钱 =", font_size=28, color=YELLOW)
        ratio_math = MathTex(r"1:4", font_size=44, color=YELLOW)
        ratio = VGroup(ratio_label, ratio_math).arrange(RIGHT, buff=0.25)
        ratio.next_to(problem, DOWN, buff=0.45)
        self.play(Write(ratio))
        self.wait(1)

        split_marks = VGroup()
        for k in range(1, 4):
            x = zhang_bar.get_left()[0] + k * zhang_bar.width / 4
            split_marks.add(Line([x, zhang_bar.get_bottom()[1], 0], [x, zhang_bar.get_top()[1], 0], color=WHITE))
        self.play(Create(split_marks))

        one_part = Rectangle(width=1.0, height=0.55, color=ORANGE, fill_color=ORANGE, fill_opacity=0.8)
        one_part.next_to(zhang_bar, RIGHT, buff=0.25)
        extra_label_text = Text("多 1 份 =", font_size=26, color=ORANGE)
        extra_label_math = MathTex(r"8 \div 4 = 2", font_size=38, color=ORANGE)
        extra_label_unit = Text("元", font_size=26, color=ORANGE)
        extra_label = VGroup(extra_label_text, extra_label_math, extra_label_unit).arrange(RIGHT, buff=0.15)
        extra_label.next_to(one_part, UP, buff=0.25)
        self.play(GrowFromEdge(one_part, LEFT), Write(extra_label))
        self.wait(1.4)

        lisi_label = Text("李四：8 + 2 = 10 元", font_size=32, color=GREEN).shift(LEFT * 3.8 + DOWN * 1.45)
        lisi_base = Rectangle(width=4.0, height=0.55, color=GREEN, fill_color=GREEN, fill_opacity=0.55)
        lisi_extra = Rectangle(width=1.0, height=0.55, color=ORANGE, fill_color=ORANGE, fill_opacity=0.85)
        lisi_bar = VGroup(lisi_base, lisi_extra).arrange(RIGHT, buff=0)
        lisi_bar.next_to(lisi_label, DOWN, buff=0.25).align_to(lisi_label, LEFT)
        self.play(FadeIn(lisi_label), GrowFromEdge(lisi_bar, LEFT))

        answer = Text("答案：李四有 10 元", font_size=44, color=GREEN).to_edge(DOWN, buff=0.55)
        answer_box = SurroundingRectangle(answer, color=YELLOW, buff=0.2)
        self.play(Write(answer), Create(answer_box))
        self.wait(1.5)

        summary_title = Text("总结", font_size=34, color=YELLOW).shift(RIGHT * 2.4 + DOWN * 0.9)
        summary1 = Text("张三的钱是比较的基准", font_size=28, color=WHITE)
        summary2_text = Text("基准 8 在分母：", font_size=28, color=ORANGE)
        summary2_math = MathTex(r"\frac{\Delta}{8}=\frac{1}{4}", font_size=38, color=ORANGE)
        summary2 = VGroup(summary2_text, summary2_math).arrange(RIGHT, buff=0.15)
        summary3 = Text("是不是一直这样呢？留给大家课后思考~", font_size=28, color=GREEN)
        summary_group = VGroup(summary_title, summary1, summary2, summary3).arrange(DOWN, buff=0.22)
        summary_group.shift(RIGHT * 2.2 + DOWN * 0.15)
        summary_box = SurroundingRectangle(summary_group, color=YELLOW, buff=0.22)
        self.play(FadeIn(summary_box), Write(summary_title))
        self.play(FadeIn(summary1, shift=UP), FadeIn(summary2, shift=UP))
        self.play(FadeIn(summary3, shift=UP))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in [
            title, problem, zhang_label, zhang_bar, ratio, split_marks,
            one_part, extra_label, lisi_label, lisi_bar, answer, answer_box,
            summary_group, summary_box,
        ]])

    # ---------- 8. 收尾 ----------
    def scene_outro(self):
        line1 = Text("分数，也可以看成比例", font_size=64, color=YELLOW)
        line2 = Text("关键：找准两个量，以及比较的基准", font_size=36, color=GREEN)
        line3 = Text("比例问题 → 分数等式 → 交叉相乘", font_size=34, color=BLUE)
        VGroup(line1, line2, line3).arrange(DOWN, buff=0.45)

        self.play(Write(line1))
        self.play(FadeIn(line2, shift=UP))
        self.play(FadeIn(line3, shift=UP))
        self.wait(2.5)

        thx = Text("下次再见！", font_size=44).to_edge(DOWN, buff=0.8)
        self.play(Write(thx))
        self.wait(2)
        self.play(FadeOut(line1), FadeOut(line2), FadeOut(line3), FadeOut(thx))

