#include <stdio.h>
#include <math.h>
#include <stdlib.h>

/* Modified Scholkman */


void peaks(const float *data, int n, int fs, int *output)
{
   // params and iterators
   int l = fs/3 - 1;
   int i=0, j=0, k=0;
   
   // 2D array
   float** Mn = (float**)malloc(n * sizeof(float*));
   for (i = 0; i < n; i++)
      Mn[i] = (float*)malloc(l * sizeof(float));
   for (i = 0; i < n; i++)
         for (j = 0; j < l; j++)
               Mn[i][j] = 0;
    
   int* Y = (int*)malloc(l * sizeof(int));
   for (i=0; i<l; ++i)
      Y[i] = 0;

   for (k=0; k<l; ++k)
   {
      for (i=k+1; i<n-k+1; ++i)
      {
        if (data[i-1] < data[i-k-1] && data[i-1] < data[i+k-1])
         {
            Y[k]++;
            Mn[i-1][k]=1;
         }
         else
         {
            Mn[i-1][k]=0;
         }
      }
   }

   int max=0, idx=0;
   for (i=0; i<l; ++i)
   {
      if (Y[i] > max)
      {
         max = Y[i];
         idx = i;
      }
   }
   free(Y);
   
   for (i=0; i<n; ++i)
      for (j=0; j<idx; ++j)
      {
         if (Mn[i][j] == 0)
            output[i]++;
      }
      
   for (i=0; i<n; ++i)
    free(Mn[i]);
}
