# class6-homework

Docker
======
A. Building the Dockerfile into an image
	docker build -t my-dataset-processor:latest .

B. Running the image 
	docker run my-dataset-processor:latest "/app/wdbc.data" "/app/wdbc_header.data"
	

Advanced
========
One of interesting plots is the pairplot (seaborn) as it allows to understand the relationships between
all possible pairs of features. In one graphic it displays the correlation and the histogram grouped by 
another categorical feature.