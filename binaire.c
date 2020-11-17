#include <stdio.h>



int main() {

    int compteur;

    int nombreAtest = 5647;

    int tab[32];
 
   int reste;

    

    for(compteur=31;compteur>=0;compteur--){

        reste = nombreAtest%2;

        tab[compteur] = reste;

        nombreAtest = nombreAtest/2;
    }


    for(compteur=0;compteur<32;compteur++){ printf("%d",tab[compteur]);}

    return 0;

} 