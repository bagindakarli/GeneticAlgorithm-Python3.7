#!/usr/bin/env python
# coding: utf-8

# In[288]:


import numpy as np
import math


# In[294]:


# pembuatan kromosom 
def kromosom_init():
    kromosom = []
    for i in range(0,4):
        kromosom.append(np.random.randint(0,10))
    return kromosom

#print(kromosom_init())


# In[301]:


# pembuatan populasi untuk menggabungkan kromosom
def populasi_init():
    populasi = []
    for i in range(0,4):
        populasi.append(kromosom_init())
    return populasi

#print(populasi_init())


# In[304]:


# pendekodean kromosom menggunakan rumus khusus untuk kromosom yang berisi integer
def dekode_kromosom(kromosom,r_min,r_max):
    sigma = 0
    sigma_k = 0
    
    for i in range(len(kromosom_a)-1):
        sigma += 10**-i
        sigma_k += kromosom[i] * sigma
    hasil_dekode = r_min + ((r_max - r_min)/9 * sigma) * sigma_k
    return hasil_dekode


# In[310]:


def div_kromosom(kromosom):
    kromosom_a = []
    kromosom_b = []
    for i in range(0,2):
        kromosom_a.append(kromosom[i])
        kromosom_b.append(kromosom[i+2])
    return kromosom_a, kromosom_b


# In[312]:


# perhitungan nilai fitness untuk mencari nilai kecocokan kromosom terhadap permasalahan. Semakin tinggi nilai fitness, maka solusi semakin optimal
def fitness(x1,x2):
    return math.cos(x1) * math.sin(x2) - x1/(x2**2 + 1)


# In[317]:


r1_min = -1
r1_max = 2
r2_min = -1
r2_max = 1
kromosom = kromosom_init()
populasi = populasi_init()
semua_fitness = []
print('populasi',populasi)

for i in range(len(populasi)):
    kromosom_a, kromosom_b = div_kromosom(populasi[i])
    hasil_dekode_a = dekode_kromosom(kromosom_a,r1_min,r1_max)
    hasil_dekode_b = dekode_kromosom(kromosom_b,r2_min,r2_max)
    
    hasil_fitness = fitness(hasil_dekode_a,hasil_dekode_b)
    semua_fitness.append(hasil_fitness)
    print()
    print(populasi[i])
    print('Hasil dekode kromosom a = ', hasil_dekode_a)
    print('Hasil dekode kromosom b = ', hasil_dekode_b)
    print('Fitness = ', hasil_fitness)


# In[324]:


# pemilihan parent dengan menggunakan metode stochastic roulette
def pilih_parent(semua_fitness):
    # stochastic roulette
    cek = True
    fitness_maks = max(semua_fitness)
    while(cek):
        indeks = round(np.random.uniform()*len(semua_fitness)-1)
        r = np.random.uniform()
        if (r < semua_fitness[indeks]/fitness_maks):
            cek = False
    return indeks;


# In[331]:


parent_1 = pilih_parent(semua_fitness)
parent_2 = pilih_parent(semua_fitness)

print('Parent 1 = ', parent_1, populasi[parent_1])
print('Parent 2 = ', parent_2, populasi[parent_2])


# In[334]:


# proses pindah silang yang dilakukan untuk membentuk dua kromosom anak baru dari dua parent yang terpilih
def crossover(parent_1, parent_2):
    kromosom_a, kromosom_b = div_kromosom(parent_1)
    kromosom_c, kromosom_d = div_kromosom(parent_2)
    
    child_1 = []
    child_2 = []
    
    child_1.append(kromosom_a+kromosom_d)
    child_2.append(kromosom_c+kromosom_b)
    
    return child_1, child_2


# In[337]:


child_1, child_2 = crossover(populasi[parent_1],populasi[parent_2])
semua_child = []
semua_child.append(child_1)
semua_child.append(child_2)

print('Parent 1: ', populasi[parent_1])
print('Parent 2: ', populasi[parent_2])
print()
print('Child 1: ', child_1)
print('Child 2: ', child_2)
print()

print('Semua Child: ', semua_child)


# In[341]:


# proses mutasi yang dilakukan untuk mengganti suatu gen dengan gen yang baru
def mutasi(child_1, child_2):
    probs = np.random.randint(0,100)
    if probs == 1:
        indeks = np.random.randint(0,len(child_1)-1)
        child_1[indeks] = np.random.randint(0,10)
    elif probs == 2:
        indeks = np.random.randint(0,len(child_2)-1)
        child_2[indeks] = np.random.randint(0,10)


# In[347]:


# proses penggantian generasi untuk memilih kromosom terbaik untuk selanjutnya akan dijadikan populasi untuk generasi berikutnya
def generasi_baru(semua_fitness, populasi, semua_child):
    # proses ini menggunakan metode seleksi fitness based selection
    kromosom_baru = []
    populasi_baru = []
    
    if (semua_fitness[0] < semua_fitness[1]):
        min_a = 0
        min_b = 1
    else:
        min_a = 1
        min_b =0
        
    for i in range(2, len(semua_fitness)):
        if (semua_fitness[i] < semua_fitness[min_b]):
            if(semua_fitness[i] < semua_fitness[min_a]):
                min_b = min_a
                min_a = i
            else:
                min_b = i
                
    for j in range(len(populasi)):
        if (j == min_a):
            kromosom_baru.append(semua_child[0])
            pop = []
            child_a, child_b = div_kromosom(semua_child[0])
            pop.append(dekode_kromosom(child_a,r1_min,r1_max))
            pop.append(dekode_kromosom(child_b,r2_min,r2_max))
            populasi_baru.append(pop)
            
        elif (j == min_b):
            kromosom_baru.append(semua_child[1])
            pop = []
            child_a, child_b = div_kromosom(semua_child[1])
            pop.append(dekode_kromosom(child_a,r1_min,r1_max))
            pop.append(dekode_kromosom(child_b,r2_min,r2_max))
            populasi_baru.append(pop)
            
        else:
            kromosom_baru.append(semua_child[j])
            pop = []
            child_a, child_b = div_kromosom(semua_child[j])
            pop.append(dekode_kromosom(child_a,r1_min,r1_max))
            pop.append(dekode_kromosom(child_b,r2_min,r2_max))
            populasi_baru.append(pop)
            
    return populasi_baru, kromosom_baru
    print(semua_child[1])


# In[351]:


#ganti_generasi(semua_fitness,populasi,semua_child)

generasi = 0
generasi_maks = 100

while (generasi < generasi_maks):
    generasi += 1
    parent_a = pilih_parent(semua_fitness)
    parent_b = pilih_parent(semua_fitness)
    i = 0
    while (parent_a == parent_b):
        i += 1
        parent_b = pilih_parent(semua_fitness)
        if (i < generasi_maks):
            break;

