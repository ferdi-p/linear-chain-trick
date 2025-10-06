from __future__ import annotations

def background_markdown() -> str:
    return r'''
**Linear-chain trick (summary)**

<p align="center">
  <img src="static/diagram-2.svg" width="80%" />
</p>


We represent a delay as a sequence of $k$ identical first-order stages.  
Choosing
$$ r = \frac{k}{\mu}$$



sets the mean delay to $\mu$.

**ODEs (content in each sub-stage):**
$$
\dot J_1 = r(0 - J_1), \qquad
\dot J_i = r(J_{i-1} - J_i), \quad i=2,\ldots,k,
$$
with initial condition $J_1(0)=1$ and $J_i(0)=0$ for $i>1$.

**Delay density (outflow of last stage):**
$$
p(t) = r\,J_k(t)
$$
which matches the Erlang/gamma pdf (shape $k$, scale $\theta=\mu/k$):
$$
p(t) = \frac{t^{k-1} e^{-t/\theta}}{\Gamma(k)\,\theta^k},\qquad \theta=\frac{\mu}{k}.
$$

**Properties:** $\mathbb{E}[T]=\mu$, $\mathrm{Var}[T]=\mu/k$, and for $k>1$ the mode is
$$
t_{\text{mode}}=\frac{k-1}{k}\,\mu.
$$
'''
