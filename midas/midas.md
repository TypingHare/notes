# MIDAS

1. **Input preparation**. For each cell $n$, we have $(x_n, s_n)$, where $x_n$ is the available multimodal count data, $s_n$ is the cell's batch ID.
2. **Modality-specific encoding**. Latent state: $z_n = (c_n, u_n)$, where $c_n$ is the biological state and $u_n$ is the technical noise. Output is A collection of modality-specific posterior estimates. There are four encoders: RNA, ADT, ATAC, Batch encoders.
3. **Product-of-experts (PoE) fusion**. Input is the posterior estimate from every modality available for the cell, together with the batch-related estimate. PoE combines available estimates into a single posterior distribution. Output is a joint posterior for the cell
   $$
   q(c_n, u_n \mid x_n, s_n)
   $$
1. **Self-supervised modality alignment**. MIDAS asks each individual modality to infer approximately the same latent state for the same cell. For a trimodal cell $\text{zRNA} \approx \text{zADT} \approx \text{zATAC}$.
2. **Biological–technical disentanglement**. Input is the joint latent variables inferred from the counts, $x_n$, and batch ID $s_n$. The model discourages the biological state $c_n$ from containing batch information.
3. **Generative reconstruction through modality decoders**. Input is a sampled or estimated latent pair $(c_n, u_n)$. Separate decoders reconstruct each modality.
4. **Low-dimensional mosaic integration**. Input is the trained joint posterior $q(c_n, u_n | x_n, s_n)$. Outputs are two cell-by-latent-dimension matrices: biological-state matrix $C = [\mu_1^c, \mu_2^c, \dots]$ and technical-noise matrix $U =[\mu_1^u, \mu_2^u, \dots]$. The paper uses a 32-dimensional biological state and a 2-dimensional technical-noise state in its implementation.
5. **Modality and missing-feature imputation**. For each cell, its inferred latent estimates $(\mu_n^c, \mu_n^u)$ are passed through all modality decoders. Output is a complete set of modalities for every cell: $c_n^R$, $c_n^A$, $c_n^D$.
6. **Batch-effect removal in feature space**. Inputs are $c_n$, $u_n$, and batch membership. MIDAS first calculates the average technical-noise vector for each batch: $\bar{u}_b$. It then identifies a representative batch whose average technical state is closest to the average technical state across all batches. For every cell, MIDAS replaces its original technical-noise vector with this common standard vector:
   $$
   (c_n, u_n) \rightarrow (c_n, \bar{u}_{\text{s}})
   $$
   Outputs are batch-corrected and imputed feature matrices.
1. **Downstream analysis**.