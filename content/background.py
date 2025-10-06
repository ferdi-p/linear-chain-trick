from __future__ import annotations

def background_markdown() -> str:
    return r'''
**Linear Chain Trick**

The Linear Chain Trick is used to implement time delays in models.

It divides a stage $J$ into $n$ sub-stages $J_i$.

<p  style="padding:25px;  align="center">
  <img src="static/diagram.svg" width="95%" />
</p>

Where the transition rate is $r=\frac{n}{\mu}$. With a single stage, the delay is exponentially distributed. With more sub-stages, the distribution becomes more narrow (it follows a Gamma Distribution).

The mean delay is independent of the number of sub-stages.

$$ mean = \mu$$

The variance of the delay decreases with the number of sub-stages.

$$ var = \frac{\mu^2}{n}$$

**ODEs**

The differential equations are

$$ \frac{d J_1}{dt}  =  \text{recruitment} - r J_1$$

And for $i=2,\ldots,n$

$$ \frac{d J_i}{dt}  =  r (J_{i-1} - J_i) $$

The maturation rate is given by individuals leaving the last stage

$$ maturation = r J_n$$

**Showing the distribution**

For the demonstration, we show the probability density function of the delay distribution. Technically, we follow single cohort and show their $maturation$ rate.

The cohort starts with

$$ J_1(0) = 1$$

While for $i=2,\ldots,n$

$$ J_i(0) = 0 $$

And there is no recruitment

$$
recruitment = 0
$$

**References**

Smith, H. (2010). *Distributed delay equations and the linear chain trick.*  
_In An Introduction to Delay Differential Equations with Applications to the Life Sciences_ (pp. 119–130). Springer New York.  
[https://link.springer.com/chapter/10.1007/978-1-4419-7646-8_7](https://link.springer.com/chapter/10.1007/978-1-4419-7646-8_7)

**Contact**

Code by Ferdinand Pfab

[ferdinand.pfab@gmail.com](mailto:ferdinand.pfab@gmail.com)

'''
