population = rnorm(1000000, mean = 100, sd = 15)

hist(population, breaks = 1:200)
mean(population)

stichprobe = sample(population, size = 10000)
hist(stichprobe, breaks = 1:200)
mean(stichprobe)

means = c()



