# engineerka
Graduation project

An accessory for bikers to judge their current speed based on experience based on. Project will be limited to camera, Raspberry Pi, LED light and software development.

Example result of trajectory prediction, where blue line is trajectory, red dot is an apex point and gray lines road edges from segmented image.
<img width="263" alt="image" src="https://user-images.githubusercontent.com/79313551/224175763-6bb5d822-cb8f-4267-bcd6-800801b1c29c.png">

A comparison between original and segmented image:
![image](https://user-images.githubusercontent.com/79313551/224176356-fd68f626-78fc-4146-aad4-4c8664b14a5b.png)

More tested images with handly selected great and terrific segmentations:
<img width="296" alt="image" src="https://user-images.githubusercontent.com/79313551/224176667-b8a3a69a-6200-4cd1-adbb-805a32b339b2.png">

Roadmap:
1. Gather Data. DONE
2. Label images. DONE
3. Build a image segmentation model in pytorch. DONE
4. Reality translator in NumPy road to plot. DONE
5. Plot to 2-3 quadratics. DONE
6. Quadratics into road line with OpenCV. DONE
