library(tidyverse)

download_logo_team <- function(id_team) {
  url <- glue::glue("https://media.api-sports.io/football/teams/{id_team}.png")
  path_logo <- glue::glue("results/logo_{id_team}.png")
  download.file(url, destfile = path_logo)
  img <- png::readPNG(path_logo, native = TRUE)
  return(img)
}

pression_index <- read_csv("/workdir/data/pression_index_135_2022.csv")
teams_id <- pression_index$team_id
for (team in teams_id) {
  download_logo_team(team)
}