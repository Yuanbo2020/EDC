<div align="center"> 
For the souce code, please see <a href="https://github.com/Yuanbo2020/EDC/tree/main/Code" 
target="https://github.com/Yuanbo2020/EDC/tree/main/Code/">here</a>.
</div>

## Feature comparison (Best viewed in color) 
![Image](Comparison_fig.1.png)
<div align="center"> 
 Subgraph: (a) Log mel spectrogram; (b) Features after the self-attention; (c) Features after EDC.  
</div>

<!-- 在此处写注释-->
<!--
<img src="../samples/Comparison_fig.1.png" width=50%/>
-->

## A detection demo of the siren sound clip
![Image](demo_of_the_siren_sound_clip.png)
<div align="center"> 
Subgraph: (a) Log mel spectrogram; (b) Bottleneck features from the trainable self-attention layer; (c) Acoustic features after EDC; (d) The probability of events
predicted by the model trained with EDC.   
</div>

## Visualization of frame-level representations distribution
![Image](tsne.png)
<div align="center"> 
Visualization of frame-level representations distribution using unsupervised t-SNE.<br>
Please note that models in this paper are trained by clip-level weak labels in datasets of DCASE and CHiME, and the label of each audio clip is a multi-hot vector, so the label corresponding to the frame-level representation is unknowable.  
</div>

## The calculation procedure of EDC
![Image](EDC_procedure.png)
<div align="center"> 
For the souce code, please see <a href="https://github.com/Yuanbo2020/EDC/tree/main/Code" 
target="https://github.com/Yuanbo2020/EDC/tree/main/Code/">here</a>.
</div>

## Attenuation curves of different alpha
![Image](different_alphas.png)
<div align="center"> 
Assuming that the attenuation starts from frame 0
</div>
 
## Further comparison of the effects of EDC
### Sample 1
![Image](sample1.png)

### Sample 2
![Image](sample2.png)

### Sample 3
![Image](sample3.png)

### Sample 4
![Image](sample4.png)

### Sample 5
![Image](sample5.png)

### Sample 6
![Image](sample6.png)

### Sample 7
![Image](sample7.png)
 
