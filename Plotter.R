
png(file="1.png", width =6, height = 6, units = "in", res = 300)

df <- data.frame(PF = rnorm(100000, mean = 100, sd = 15))
ggplot(df, aes(x = PF)) +
  geom_histogram(aes(y =..density..),
                 breaks = seq(50, 150, by = 2),
                 colour = "black",
                 fill = "white", bins = 100) +
  scale_x_continuous( breaks = seq(50, 150, by = 50)) +
  #stat_function(fun = dnorm, args = list(mean = mean(df$PF), sd = sd(df$PF))) +
  labs(x = "IQ", y = "relative Häufigkeit") +
  theme_classic() +
  theme(text = element_text(size = 25))

dev.off()

png(file="2.png", width =6, height = 6, units = "in", res = 300)

df <- data.frame(PF = rnorm(100000, mean = 100, sd = 15))
ggplot(df, aes(x = PF)) +
  # geom_histogram(aes(y =..density..),
  #                breaks = seq(50, 150, by = 2),
  #                colour = "black",
  #                fill = "white", bins = 100) +
  scale_x_continuous( breaks = seq(50, 150, by = 50)) +
  stat_function(fun = dnorm, args = list(mean = mean(df$PF), sd = sd(df$PF))) +
  labs(x = "IQ", y = "Dichte") +
  theme_classic() +
  theme(text = element_text(size = 25))

dev.off()

png(file="3.png", width =6, height = 6, units = "in", res = 300)

df <- data.frame(PF = rnorm(50, mean = 100, sd = 15))
ggplot(df, aes(x = PF)) +
  geom_histogram(aes(y =..density..),
                 breaks = seq(50, 150, by = 2),
                 colour = "black",
                 fill = "white", bins = 30) +
  scale_x_continuous( breaks = seq(50, 150, by = 50)) +
  #stat_function(fun = dnorm, args = list(mean = mean(df$PF), sd = sd(df$PF))) +
  labs(x = "IQ", y = "rel. Häufigkeit") +
  theme_classic() +
  theme(text = element_blank())

dev.off()

png(file="4.png", width =6, height = 6, units = "in", res = 300)

df <- data.frame(PF = rnorm(50, mean = 100, sd = 15))
ggplot(df, aes(x = PF)) +
  geom_histogram(aes(y =..density..),
                 breaks = seq(50, 150, by = 2),
                 colour = "black",
                 fill = "white", bins = 30) +
  scale_x_continuous( breaks = seq(50, 150, by = 50)) +
  #stat_function(fun = dnorm, args = list(mean = mean(df$PF), sd = sd(df$PF))) +
  labs(x = "IQ", y = "rel. Häufigkeit") +
  theme_classic() +
  theme(text = element_blank())

dev.off()

png(file="5.png", width =6, height = 6, units = "in", res = 300)

df <- data.frame(PF = rnorm(50, mean = 100, sd = 15))
ggplot(df, aes(x = PF)) +
  geom_histogram(aes(y =..density..),
                 breaks = seq(50, 150, by = 2),
                 colour = "black",
                 fill = "white", bins = 30) +
  scale_x_continuous( breaks = seq(50, 150, by = 50)) +
  #stat_function(fun = dnorm, args = list(mean = mean(df$PF), sd = sd(df$PF))) +
  labs(x = "IQ", y = "rel. Häufigkeit") +
  theme_classic() +
  theme(text = element_blank())

dev.off()

png(file="6.png", width =6, height = 6, units = "in", res = 300)

df <- data.frame(PF = rnorm(50, mean = 100, sd = 15))
ggplot(df, aes(x = PF)) +
  geom_histogram(aes(y =..density..),
                 breaks = seq(50, 150, by = 2),
                 colour = "black",
                 fill = "white", bins = 30) +
  scale_x_continuous( breaks = seq(50, 150, by = 50)) +
  #stat_function(fun = dnorm, args = list(mean = mean(df$PF), sd = sd(df$PF))) +
  labs(x = "IQ", y = "rel. Häufigkeit") +
  theme_classic() +
  theme(text = element_blank())

dev.off()

