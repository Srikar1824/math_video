# Individual Viva / Q&A Defense Notes
**Project:** Eigenvalues and Eigenvectors — Visualizing Invariant Directions  
**Student:** Srikar Burgu (`E25B070605`)  
**Course:** Linear Algebra and Calculus (M3)

Use these concise notes to answer any instructor questions about the mathematics, visual design, and animation code during your Q&A session.

---

## 1. Mathematical Questions & Derivations

### Q1: What is an eigenvector and an eigenvalue in plain geometric terms?
- **Answer:** When a square matrix $A$ acts as a linear transformation on space, almost every vector is rotated off its original line (span). An **eigenvector** $\vec{v} \neq \mathbf{0}$ is a special non-zero vector that *refuses to rotate*—it stays strictly on its original span line. The **eigenvalue** $\lambda$ is the scalar factor by which that eigenvector is stretched, shrunk, or flipped ($\lambda < 0$).

### Q2: Why must $\vec{v}$ be non-zero in $A\vec{v} = \lambda \vec{v}$?
- **Answer:** If $\vec{v} = \mathbf{0}$, then $A\mathbf{0} = \mathbf{0} = \lambda \mathbf{0}$ is trivially true for *every* number $\lambda$, which gives no meaningful directional information about the transformation $A$.

### Q3: Why do we set $\det(A - \lambda I) = 0$?
- **Answer:** Rearranging $A\vec{v} = \lambda\vec{v}$ gives $(A - \lambda I)\vec{v} = \mathbf{0}$. For a **non-zero** vector $\vec{v}$ to map to the zero vector $\mathbf{0}$, the matrix $(A - \lambda I)$ must be **singular** (non-invertible)—meaning it squashes space into a lower dimension (its null space is non-trivial). A square matrix is singular if and only if its determinant is zero: $\det(A - \lambda I) = 0$.

### Q4: Walk through your worked example $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ by hand.
1. **Characteristic Polynomial:**
   $$\det(A - \lambda I) = \begin{vmatrix} 2-\lambda & 1 \\ 1 & 2-\lambda \end{vmatrix} = (2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0$$
2. **Factoring:**
   $$(\lambda - 3)(\lambda - 1) = 0 \implies \lambda_1 = 3, \quad \lambda_2 = 1$$
3. **Eigenvector for $\lambda_1 = 3$:**
   $$(A - 3I)\vec{v}_1 = \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies -x + y = 0 \implies y = x \implies \vec{v}_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$$
   *Verification:* $A\vec{v}_1 = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}\begin{pmatrix} 1 \\ 1 \end{pmatrix} = \begin{pmatrix} 3 \\ 3 \end{pmatrix} = 3\begin{pmatrix} 1 \\ 1 \end{pmatrix}$. Matches!
4. **Eigenvector for $\lambda_2 = 1$:**
   $$(A - I)\vec{v}_2 = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix} \implies x + y = 0 \implies y = -x \implies \vec{v}_2 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$$
   *Verification:* $A\vec{v}_2 = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}\begin{pmatrix} 1 \\ -1 \end{pmatrix} = \begin{pmatrix} 1 \\ -1 \end{pmatrix} = 1\begin{pmatrix} 1 \\ -1 \end{pmatrix}$. Matches!

### Q5: Why are the two eigenvectors perpendicular in your example?
- **Answer:** Because $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ is a **real symmetric matrix** ($A = A^T$). By the **Spectral Theorem**, eigenvectors corresponding to distinct eigenvalues of a real symmetric matrix are always orthogonal ($\vec{v}_1 \cdot \vec{v}_2 = 1(1) + 1(-1) = 0$).

---

## 2. Visual & Code Questions

### Q6: Why did you choose these colors and grid animations?
- **Answer:** I followed a clean, high-contrast dark theme (inspired by 3Blue1Brown) so equations remain crisp at 1080p. I used consistent color coding: **Gold** for the matrix $A$, **Orange/Pink** for the non-eigenvector $\vec{w} = (1, 2)^T$ that visibly rotates off its span line, **Emerald Green** for $\vec{v}_1 = (1, 1)^T$ ($\lambda_1 = 3$), and **Sky Blue** for $\vec{v}_2 = (1, -1)^T$ ($\lambda_2 = 1$).

### Q7: How does your Python code generate the video?
- **Answer:**
  - `render_video.py` computes the frame index `t = frame_idx / 30.0` at 30 fps (`1920x1080`), linearly interpolates the transformation matrix $M(t) = (1 - \alpha)I + \alpha A$ to deform every grid line and vector smoothly, draws the overlays with Pillow (`ImageDraw`), and pipes raw RGB24 frames directly into `ffmpeg` (`libx264`, `yuv420p`) alongside the mixed voice-over audio track.
  - `manim_eigenvalues.py` provides the equivalent scene-by-scene structure using the Manim Community API (`NumberPlane`, `MathTex`, `apply_matrix`).

### Q8: How did you synchronize the visuals to your voice-over?
- **Answer:** I transcribed the 5:39 voice-over recording using `whisper.cpp` to extract exact timestamps (`.srt`) for every scene transition (0:00, 0:51.3, 1:33.8, 2:32.3, 4:23.9, 5:13.0) and key spoken cues (such as when the orange, green, and blue vectors are introduced).
