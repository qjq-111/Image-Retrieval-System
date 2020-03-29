# Image-Retrieval-System
Image retrieval system developed by Django.

### Requirements
  * python 3.X <br>
  * pytorch 0.4 <br>
  * django 2.1.4

### Inspiration
  * Text retrieval can not meet our needs sometimes, we need a image retrieval system. <br>
  * Deep learning has powerful abality to extract image features. <br>
  * Hash method for image retrieval has speed advantage when facing big image retrieval database.
  
### Instructions
  * The model borrows from DPSH.<br>
  * The system regard nus-wide dataset as image retrieval database.<br>
  * the image databse stores in '/mageSearch/static/ImageSearch/image/'<br>
  * It shows the top five images which are the most similar to the uploaded images.<br>
  * The uploaded image would store in '/mageSearch/static/ImageSearch/image/upload/'<br>
  * The system can record the upload time adn the hash code and name of the uploaded image in Sqlite.
  
### Demonstration
  ![image](https://github.com/La-ji/Image-Retrieval-System/blob/master/Demonstration/search.png)
 
