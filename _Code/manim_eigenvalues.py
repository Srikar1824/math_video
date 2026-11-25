"""
=============================================================================
Linear Algebra & Calculus (M3) - Internal Assessment: Animation Project
Project: Eigenvalues and Eigenvectors (Visualizing Invariant Directions)
Student: Srikar Burgu
Student ID: E25B070605
=============================================================================
This file contains the complete Manim Python script defining all 6 scenes 
for the programmatic animation video according to M3 syllabus requirements.
"""

from manim import *
import numpy as np

class EigenvaluesFullVideo(Scene):
    def construct(self):
        # 1. Opening Frame
        self.opening_frame()
        # 2. Scene 1: Hook
        self.scene_1_hook()
        # 3. Scene 2: Concept Intro
        self.scene_2_concept_intro()
        # 4. Scene 3: Visual Intuition
        self.scene_3_visual_intuition()
        # 5. Scene 4: Worked Example
        self.scene_4_worked_example()
        # 6. Scene 5: Interpretation
        self.scene_5_interpretation()
        # 7. Scene 6: Summary & Closing Credits
        self.scene_6_summary_credits()

    def opening_frame(self):
        title = Text("EIGENVALUES & EIGENVECTORS", font_size=44, color=WHITE, weight=BOLD)
        subtitle = Text("Visualizing Invariant Directions of Linear Transformations", font_size=24, color=TEAL)
        subtitle.next_to(title, DOWN, buff=0.3)
        
        info_card = VGroup(
            Text("Linear Algebra & Calculus (M3) • Internal Assessment", font_size=20, color=GOLD),
            Text("Student: Srikar Burgu  |  ID: E25B070605", font_size=22, color=LIGHT_GRAY),
            Text("Target Duration: ~5 Minutes | 1080p 16:9 Landscape", font_size=18, color=GRAY)
        ).arrange(DOWN, buff=0.2).next_to(subtitle, DOWN, buff=0.6)
        
        self.play(FadeIn(title, shift=UP), FadeIn(subtitle, shift=UP), run_time=1.5)
        self.play(FadeIn(info_card, shift=UP), run_time=1.5)
        self.wait(3.0)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(info_card), run_time=1.0)

    def scene_1_hook(self):
        header = Text("Scene 1: How Linear Transformations Warp Space", font_size=28, color=TEAL).to_edge(UP)
        self.play(Write(header))
        
        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-3, 3, 1],
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1, "stroke_opacity": 0.6}
        )
        self.play(Create(plane), run_time=1.5)
        
        v1 = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(2, 1), color=ORANGE, buff=0)
        v2 = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(-1, 2), color=PINK, buff=0)
        self.play(GrowArrow(v1), GrowArrow(v2))
        
        # Matrix deformation
        matrix = [[1.8, 0.8], [0.5, 1.4]]
        self.play(
            plane.animate.apply_matrix(matrix),
            v1.animate.put_start_and_end_on(plane.coords_to_point(0, 0), plane.coords_to_point(2*1.8 + 1*0.8, 2*0.5 + 1*1.4)),
            run_time=4.0
        )
        
        q_text = Text("Are there special vectors that REFUSE to rotate?", font_size=26, color=GOLD)
        q_text.to_edge(DOWN)
        self.play(FadeIn(q_text))
        self.wait(2.0)
        self.play(FadeOut(plane), FadeOut(v1), FadeOut(v2), FadeOut(q_text), FadeOut(header))

    def scene_2_concept_intro(self):
        header = Text("Scene 2: Concept Introduction & Notation", font_size=28, color=TEAL).to_edge(UP)
        formula = MathTex(r"A \vec{v} = \lambda \vec{v}", font_size=64)
        
        t_A = MathTex(r"A \text{ : Square Transformation Matrix }(n \times n)", font_size=26, color=GOLD)
        t_v = MathTex(r"\vec{v} \text{ : Non-zero Eigenvector (Invariant Direction)}", font_size=26, color=GREEN)
        t_l = MathTex(r"\lambda \text{ : Eigenvalue (Scalar Stretch Factor)}", font_size=26, color=BLUE)
        
        breakdown = VGroup(t_A, t_v, t_l).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(formula, DOWN, buff=0.8)
        
        self.play(Write(header))
        self.play(Write(formula), run_time=2.0)
        self.play(LaggedStart(FadeIn(t_A, shift=RIGHT), FadeIn(t_v, shift=RIGHT), FadeIn(t_l, shift=RIGHT), lag_ratio=0.5))
        self.wait(3.0)
        self.play(FadeOut(formula), FadeOut(breakdown), FadeOut(header))

    def scene_3_visual_intuition(self):
        header = Text("Scene 3: Visual Intuition (A = [[2, 1], [1, 2]])", font_size=28, color=TEAL).to_edge(UP)
        self.play(Write(header))
        
        plane = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1])
        self.play(Create(plane))
        
        # Invariant line y = x (Green) and y = -x (Blue)
        line_diag1 = Line(plane.coords_to_point(-3, -3), plane.coords_to_point(3, 3), color=GREEN_D, stroke_width=2)
        line_diag2 = Line(plane.coords_to_point(-3, 3), plane.coords_to_point(3, -3), color=BLUE_D, stroke_width=2)
        
        v_green = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(1, 1), color=GREEN, buff=0)
        v_blue = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(1, -1), color=BLUE, buff=0)
        v_orange = Arrow(plane.coords_to_point(0, 0), plane.coords_to_point(1, 2), color=ORANGE, buff=0)
        
        self.play(Create(line_diag1), Create(line_diag2))
        self.play(GrowArrow(v_green), GrowArrow(v_blue), GrowArrow(v_orange))
        
        # Transform by A = [[2, 1], [1, 2]]
        # v_green (1, 1) -> (3, 3) = 3 * v_green
        # v_blue (1, -1) -> (1, -1) = 1 * v_blue
        # v_orange (1, 2) -> (4, 5) (rotates)
        self.play(
            plane.animate.apply_matrix([[2, 1], [1, 2]]),
            v_green.animate.put_start_and_end_on(plane.coords_to_point(0, 0), plane.coords_to_point(3, 3)),
            v_blue.animate.put_start_and_end_on(plane.coords_to_point(0, 0), plane.coords_to_point(1, -1)),
            v_orange.animate.put_start_and_end_on(plane.coords_to_point(0, 0), plane.coords_to_point(4, 5)),
            run_time=4.0
        )
        self.wait(2.0)
        self.play(FadeOut(plane), FadeOut(v_green), FadeOut(v_blue), FadeOut(v_orange), FadeOut(line_diag1), FadeOut(line_diag2), FadeOut(header))

    def scene_4_worked_example(self):
        header = Text("Scene 4: The Worked Example (Algebraic Derivation)", font_size=28, color=TEAL).to_edge(UP)
        self.play(Write(header))
        
        eq1 = MathTex(r"\det(A - \lambda I) = 0", font_size=38, color=GOLD)
        eq2 = MathTex(r"\begin{vmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{vmatrix} = (2-\lambda)^2 - 1 = 0", font_size=32)
        eq3 = MathTex(r"\lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0", font_size=32)
        res_eval = MathTex(r"\implies \lambda_1 = 3, \quad \lambda_2 = 1", font_size=36, color=GREEN)
        
        v1_eq = MathTex(r"\text{For } \lambda_1 = 3: \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = 0 \implies y = x \implies \vec{v}_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}", font_size=28)
        v2_eq = MathTex(r"\text{For } \lambda_2 = 1: \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = 0 \implies y = -x \implies \vec{v}_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}", font_size=28)
        
        all_eqs = VGroup(eq1, eq2, eq3, res_eval, v1_eq, v2_eq).arrange(DOWN, buff=0.35).next_to(header, DOWN, buff=0.5)
        
        for eq in all_eqs:
            self.play(Write(eq), run_time=1.5)
            self.wait(1.0)
        self.wait(2.0)
        self.play(FadeOut(all_eqs), FadeOut(header))

    def scene_5_interpretation(self):
        header = Text("Scene 5: Geometric Interpretation & Applications", font_size=28, color=TEAL).to_edge(UP)
        self.play(Write(header))
        
        card1 = Text("• Google PageRank: Dominant eigenvector ranks web pages", font_size=24, color=GOLD)
        card2 = Text("• Principal Component Analysis (PCA): Eigenvectors find maximal variance in ML", font_size=24, color=BLUE)
        card3 = Text("• Structural Resonance: Eigenvalues determine natural frequencies of bridges", font_size=24, color=GREEN)
        
        group = VGroup(card1, card2, card3).arrange(DOWN, aligned_edge=LEFT, buff=0.6).center()
        self.play(LaggedStart(FadeIn(card1), FadeIn(card2), FadeIn(card3), lag_ratio=0.5))
        self.wait(3.0)
        self.play(FadeOut(group), FadeOut(header))

    def scene_6_summary_credits(self):
        title = Text("3 Core Takeaways & Summary", font_size=36, color=GOLD).to_edge(UP)
        t1 = Text("1. Invariant Directions: Eigenvectors never rotate under transformation.", font_size=22)
        t2 = Text("2. Scaling Factors: Eigenvalues quantify stretch factor along each axis.", font_size=22)
        t3 = Text("3. Algebraic Solution: Solved via det(A - λI) = 0.", font_size=22)
        
        takeaways = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)
        
        credits_box = VGroup(
            Text("Linear Algebra and Calculus (M3) • Internal Assessment", font_size=20, color=TEAL),
            Text("Student: Srikar Burgu  |  ID: E25B070605", font_size=22, color=WHITE),
            Text("Code: Python, Manim, Matplotlib, FFmpeg  |  Narration: Srikar Burgu", font_size=18, color=GRAY),
            Text("AI Tool Disclosure: Used for scripting and animation coding assistance.", font_size=16, color=LIGHT_GRAY)
        ).arrange(DOWN, buff=0.2).next_to(takeaways, DOWN, buff=0.8)
        
        self.play(Write(title))
        self.play(FadeIn(takeaways, shift=UP))
        self.play(FadeIn(credits_box, shift=UP))
        self.wait(4.0)
