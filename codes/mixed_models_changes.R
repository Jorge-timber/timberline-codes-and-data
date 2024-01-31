setwd('C:/Users/Jorge Glez/OneDrive - Universidad de Oviedo/MASTER_GIS/TFM/DINAMICA/glmm/r_glmm')
rm(list = ls())
library(lme4)
library(sp)
library(sf)

##Data input and pre-processing
data<-st_read("datos_cinco.shp")
data<-na.exclude(data)
data$TIPO <- factor(data$TIPO, levels = c("Abedulares", "Hayedos acidofilos", "Hayedos basofilos", "Robledales acidofilos", "Robledales orocantabrica"))
data_1575 <- subset(data, mdt02_buen >= 1575)


#model fitting
model <- lmer(var_alt ~ TIPO + eastness + northness + pendiente + (1 | fid), data = data_1575)
summary(model)
var <- drop1(model, test = "Chisq")
var

