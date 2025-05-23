Cluster and visualize similar images. Feature extraction with pre-trained models from TensorFlow.

#### Suggested way to run the project

It is suggested to run with docker, using the base image `tensorflow/tensorflow:latest-gpu-jupyter`. Adapt the following command:

`sudo docker run --runtime=nvidia --gpus all --shm-size 8G --name keras_jupyter_birds -p 8888:8888 -p 8852:8851 -v {your_repository_dir}:/tf/birds  tensorflow/tensorflow:latest-gpu-jupyter`

Then:

`sudo docker exec -it keras_jupyter_birds bash`<br>
`cd birds`<br>
`pip install --ignore-installed -r requirements.txt`

#### Overall structure

In the Jupyter Notebook - Feature Extraction - you will be able obtain the Principal Components from VGG16 feature extractions on images present on `/data`. You will also be able to conduct elbow analysis to figure out how many different clusters are adequate for the dataset.
The output of this phase is a csv with the belonging cluster of each image and their first 3 main dimensions from Principal Component Analysis for further plotting.

To run the dashboard for visualizing the clusters, within the container run:

`python pca_cluster.py`<br>

Then acess: `localhost:8852` on your browser.

The data for the results here presented came from the following Kaggle dataset:

https://www.kaggle.com/datasets/umairshahpirzada/birds-20-species-image-classification

[Clustering Birds.webm](https://github.com/user-attachments/assets/8b09b372-ddc8-478b-9590-fd43d4db85b0)




