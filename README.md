# M3 Internal Assessment: Eigenvalues and Eigenvectors

**Visualizing Invariant Directions of Linear Transformations**

- **Course:** Linear Algebra and Calculus (M3)
- **Student Name:** Srikar Burgu
- **Student ID:** `E25B070605`
- **Duration:** 5 minutes 39 seconds (`1920x1080` 16:9 Landscape MP4)

---

## Repository Structure

- `math vid 1.mp4` *(or `_Video.mp4`)* — Final rendered 1080p 16:9 animation video with synchronized voice-over narration, opening title frame, smooth transitions, and closing credits (stored locally / uploaded separately).
- [`_Code/`](_Code/) — Complete Python animation source code:
  - [`_Code/render_video.py`](_Code/render_video.py) — Finalized Python/Pillow/NumPy + FFmpeg rendering pipeline (v3) with crossfade transitions, clipped 2D viewports, and exact audio timestamp synchronization.
  - [`_Code/manim_eigenvalues.py`](_Code/manim_eigenvalues.py) — Equivalent Manim Community scene script (`EigenvaluesFullVideo`).
  - [`_Code/requirements.txt`](_Code/requirements.txt) — Python dependencies.
- [`Storyboard/Storyboard.pdf`](Storyboard/Storyboard.pdf) — Official 6-scene storyboard PDF (and [`Storyboard.md`](Storyboard/Storyboard.md)).
- [`Viva_Defense_Notes.md`](Viva_Defense_Notes.md) — Mathematical & code Q&A defense notes.

---

## Mathematical Overview

Given a square transformation matrix $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$:
- **Characteristic Equation:** $\det(A - \lambda I) = (2 - \lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0$
- **Eigenvalues:** $\lambda_1 = 3$, $\lambda_2 = 1$
- **Eigenvectors:** $\vec{v}_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$ (stretches by $3\times$ along $y = x$) and $\vec{v}_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$ (stays invariant along $y = -x$).

---

## Credits & AI Disclosure
- **Narration:** Original voice-over recorded by Srikar Burgu.
- **Audio & Video Tooling:** Python, Manim, NumPy, Pillow, Matplotlib, ReportLab, Whisper.cpp (for timestamp alignment), and FFmpeg.
- **AI Assistance Disclosure:** AI tools were used to assist with script structuring, timestamp alignment, and Python animation code generation.
