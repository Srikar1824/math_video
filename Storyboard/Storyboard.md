# Project Storyboard: Eigenvalues and Eigenvectors
**Linear Algebra and Calculus (M3) • Internal Assessment (10%)**

- **Student Name:** Srikar Burgu
- **Student ID:** E25B070605
- **Video Duration:** 5m 39s (Recommended: 5 min, Max: 7 min)
- **Format:** 1080p 16:9 Landscape MP4
- **Animation Framework:** Python, Manim, Matplotlib, FFmpeg

---

## One-Sentence Learning Objective
> *"By the end of this video, the viewer will be able to understand, explain, and interpret how eigenvalues and eigenvectors represent the invariant stretching axes of a 2D matrix transformation, and solve for them algebraically using the characteristic equation."*

---

## 6-Scene Detailed Storyboard

| Scene | Time | Purpose | Visual Plan | Narration & Math Plan |
| :--- | :--- | :--- | :--- | :--- |
| **Scene 1: Hook / Context** | 0:00 – 0:51 | Spark curiosity and motivate the concept of invariant directions. | • Opening frame with student details.<br/>• 2D grid continuously warps.<br/>• Multiple colorful vectors spin and rotate off their original span lines.<br/>• Big question banner appears. | *"Imagine a rubber sheet being stretched... Almost every vector rotates off its line. Are there special vectors that refuse to rotate? Yes: eigenvectors!"* |
| **Scene 2: Concept Intro** | 0:51 – 1:34 | Define formal equation and establish notation. | • Centerpiece formula: $A\vec{v} = \lambda \vec{v}$.<br/>• 3 highlight cards:<br/>  - **$A$**: Square matrix (Gold)<br/>  - **$\vec{v}$**: Eigenvector (Green)<br/>  - **$\lambda$**: Eigenvalue (Blue)<br/>• Visual scalar collapse graphic. | *"A times v equals lambda times v. Matrix multiplication acts like ordinary scalar scaling for eigenvectors. The direction remains completely invariant."* |
| **Scene 3: Visual Intuition** | 1:34 – 2:32 | Build geometric intuition on a 2D grid with a concrete matrix. | • Plane transforms by $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$.<br/>• Orange vector $(1, 2)$ rotates (NOT an eigenvector).<br/>• Green vector on $y=x$ stretches $3\times$ without tilting ($\lambda=3$).<br/>• Blue vector on $y=-x$ stays on line ($\lambda=1$). | *"Watch the orange vector tilt. Now look at the green vector on y = x: it does not tilt at all! Similarly, the blue vector on y = -x stays strictly on its line."* |
| **Scene 4: Worked Example** | 2:32 – 4:24 | Step-by-step algebraic derivation of eigenvalues and eigenvectors. | • Characteristic equation: $\det(A - \lambda I) = 0$.<br/>• Polynomial expansion: $\lambda^2 - 4\lambda + 3 = (\lambda - 3)(\lambda - 1) = 0$.<br/>• Yields $\lambda_1=3, \lambda_2=1$.<br/>• Solves $(A - \lambda I)\vec{v} = 0$ to get eigenvectors $[1, 1]^T$ and $[1, -1]^T$. | *"How do we find these values algebraically? We compute det(A - λI) = 0... expanding gives λ² - 4λ + 3 = 0. Solving gives eigenvalues 3 and 1, and eigenvectors [1, 1] and [1, -1]."* |
| **Scene 5: Interpretation** | 4:24 – 5:13 | Connect algebraic solutions back to geometry and real engineering. | • Visualizes decoupled coordinate system: independent stretches along eigen-axes.<br/>• 3 Real-World Application Cards:<br/>  1. Google PageRank<br/>  2. Principal Component Analysis (PCA)<br/>  3. Structural Vibration Modes. | *"Eigenvectors decouple complex 2D matrix transformations into simple 1D stretches. This powers Google's PageRank, PCA in data science, and resonance calculations in bridges."* |
| **Scene 6: Summary & Credits** | 5:13 – 5:39 | Reinforce core takeaways, cite tools, and disclose AI usage. | • 3 Core Takeaways bulleted on screen.<br/>• Closing title frame with student name, ID, tools (Python, Manim, Matplotlib, FFmpeg), and AI disclosure. | *"To wrap up: 1. Invariant directions that never rotate; 2. Eigenvalues give the scale factor; 3. Solved via det(A - λI) = 0. Thank you for watching!"* |

---

## Deliverables & Evaluation Readiness
1. **`_Video.mp4`**: Rendered in 1080p 16:9 MP4 format with synchronized voice narration and Opening/Closing frames.
2. **`_Code/`**: Contains full Manim script (`manim_eigenvalues.py`) and standalone rendering script (`render_video.py`).
3. **`Storyboard.pdf`**: Submitted in the repository root / `Storyboard/` directory.
4. **`Viva_Defense_Notes.md`**: Complete Q&A defense document covering derivations, geometric proofs, and code explanations.
