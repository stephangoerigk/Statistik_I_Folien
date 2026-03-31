if (!requireNamespace("pagedown", quietly = TRUE)) install.packages("pagedown")
library(pagedown)

my_local_wd <- getwd()
message(paste("Arbeitsverzeichnis:", my_local_wd))

for (i in 1:12) {
  nr_string <- sprintf("%02d", i)
  current_input <- file.path(my_local_wd, paste0("Statistik_I_", nr_string, ".html"))
  output_name <- file.path(my_local_wd, paste0("QMI_Einheit_", i, ".pdf"))

  if (!file.exists(current_input)) {
    message(paste("Überspringe Einheit", i, "- Lokale HTML-Datei nicht gefunden."))
    next
  }

  message(paste0("Verarbeite lokale Einheit ", i, "..."))

  tryCatch({
    pagedown::chrome_print(
      input = current_input,
      output = output_name,
      timeout = 120
    )
    message(paste("--> PDF erfolgreich erstellt:", output_name))
  }, error = function(e) {
    message(paste("!!! FEHLER beim Drucken von Einheit", i))
  })
}

message("--- VORGANG ABGESCHLOSSEN ---")


# Zum Drucken einzelner Foliensätze ---------------------------------------

pagedown::chrome_print("Statistik_I_01.html", timeout = 120)
