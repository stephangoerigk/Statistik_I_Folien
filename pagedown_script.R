#install.packages("pagedown")

library(pagedown)

# Basis-URL (passen Sie das Jahr auf SS26 an, wenn es soweit ist)
base_url <- "https://stephangoerigk.github.io/Statistik_I_Folien_SS24/Statistik_I_"
einheiten <- 1:11

for (i in einheiten) {
  # URL zusammenbauen (mit führender Null falls nötig, z.B. _01, _11)
  current_url <- paste0(base_url, i, "_SS24.html")
  output_name <- paste0("QMI_Einheit_", i, ".pdf")

  message(paste("Verarbeite:", current_url))

  try({
    chrome_print(current_url, output = output_name)
    message("--> Erfolg!")
  })
}
