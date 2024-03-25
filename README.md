<h2> AutoSGD -- For Space Group Determination Based on Real Space Method</h2>

<h3> Real Space Method is proposed by Yang Yi & Yang QiBin </h3>

* Institute & Ownership: XiangTan University, Hunan, China
* Paper: Novel strategy for space group determination in real space
* https://doi.org/10.1016/j.jmst.2022.04.058

<h3> Software is programed by Li Rui </h3>

* Notice: This repository is private by Now, it'll be public soon as corresponding article is published.
* GitHub:
* Address: https://github.com/Nathan464/pythonProject
* Contact: l19791215@outlook.com

<h3> Software & Version </h3>
* Python 3.7
* PyCharm 2022.3
* MySQL Server 8.0

<h3> Side-Packages & Version </h3>

|    Package    |  Version  |
|:-------------:|:---------:|
|    atomap     |   0.3.1   |
|   hyperspy    |   1.7.3   |
| opencv-python | 4.4.0.46  |
|     numpy     |  1.18.5   |
|  matplotlib   |   3.4.3   |
|    skimage    |  0.18.3   |
|     scipy     |   1.4.1   |
|    PyMySQL    |   1.0.2   |

<h3> Menu & Functions:</h3>

<h4> File Menu:  </h4>

* Image Loading: Support image file type 
  * .tif  
  * .png
  * .jpg

<h4> Mode Menu:</h4>

* "1" or "BG(Black)" -- Background is Black
* "2" or "BG(White)"-- Background is White

<h4> Peaks Finders Menu:</h4>
<h5> 1. Sub-Menu: Initial Peaks </h5>

* DoG & LoG & Local Max methods are supported by  _skimage_
* Maximum & Minimum & CoM methods are based on _Center of Mass Theory_
* Default params of each method can be found on _Package--initial_peaks.py_

<h5> 2. Sub-Menu: Initial Results </h5>

* Click to show figure with _results of Initial Peaks Finders_

<h5> 3. Sub-Menu: Refinement </h5>

* Refine initial peaks using 2D Gaussian Model
* Supported by _Atomap_ (https://atomap.org/)
* Relate article: https://doi.org/10.1186/s40679-017-0042-5

<h5> 4. Sub-Menu: Refine Results </h5>

* Click to show  _results of 2D Gaussian Model_

<h4> Calculate Menu: </h4>

<h5> 1. Sub-Menu: Search </h5> 

* Search space group using offered info

<h5> 2. Sub-Menu: Basic Vectors </h5> 

* Calculate basic vectors from 3 micrograph as preparation of calculation of real space parameters

<h5> 3. Sub-Menu: Real Space Parameters </h5> 

* Calculate real space parameters using Niggli reduced cell method proposed by Yang
* Paper: https://doi.org/10.1016/j.micron.2016.12.006

<h5> 4. Sub-Menu: Plane Group </h5> 

* Determine 2D plane group using atom positions amplitudes

<h5> 5. Sub-Menu: Space Group </h5> 

* Determine 3D space group by gathering all relate info calculated by previous steps

<h4> Result Menu: </h4>

|     Name      |                      Property                       |
|:-------------:|:---------------------------------------------------:|
| Initial Peaks | Initial peaks result calculated by selected method  |
| Refine Peaks  | Refine peaks result calculated by 2D Gaussian model |
| Basic Vectors |                Basic vectors results                |
|  Parameters   |            Real space parameters results            |
|  Plane Group  |      2D plane group results and related output      |
|  Space Group  |                3D space group result                |

<h4> Operations Menu: </h4>

* Some useful image processing methods, include Hist, FFT, Filters -- Supported mostly by opencv-python

<h4> Exit Menu: </h4>

* Exit program fully

