library(maptools)
library(sp)
library(sf)
library(spdep)

all<-st_read("todos_montano.gpkg")


### FUNCTION TO COMPUTE A LINEAR MODEL, ANOVA, AND MORAN'S I ###
# dataset: Dataset in SHP or GPKG file format.
# n: Altitude threshold represented as a quantile (ranging from 0 to 1).

ml_anova_moran<-function(dataset,n){
  
  require(sp)
  require(sf)
  require(RANN)
  require(spdep)
  #c=threshold
  c<-round(as.numeric(quantile(dataset$mdt02_bueno,probs=n)),0)
  dataset_n<-na.exclude(dataset[dataset$mdt02_bueno>c,])
  #t=sample size
  t<-length(dataset_n$mdt02_bueno)
  #mean altitude
  mean_h<-mean(dataset_n$mdt02_bueno)
  dataset_n$temp_repro<-dataset_n$temp_repro/10
  #GLM
  MOD_dataset<-lm(mdt02_bueno ~ temp_repro+rad_repro+preci_repro+eastness+northness+TRI+TPI,data = dataset_n)
  anova_dataset<-anova(MOD_dataset)
  anova_dataset<-round(as.data.frame(anova_dataset$`Sum Sq`))
  total_oro<-apply(X= anova_dataset, MARGIN=2, FUN= sum) 
  R.SQ_dataset<-round(anova_dataset/total_oro,digits=3)
  #I moran residuals
  res_dataset<-MOD_dataset$residuals
  coords <- st_coordinates(dataset_n)
  test<-knn2nb(knearneigh(coords))
  listw<-nb2listw(test)
  Imoran_dataset = moran.test(res_dataset,listw)
  
  return(list(t,mean_h,summary(MOD_dataset),R.SQ_dataset,Imoran_dataset))
}


#example

ml_anova_moran(all,0.5)
ml_anova_moran(all,0.75)
