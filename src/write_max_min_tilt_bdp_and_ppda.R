library(tidyverse)

league = "135"
path <- glue::glue("/workdir/data/pression_index_{league}_2022.csv")
tilt_bdp_ppda <- read_csv(path)
max_min_tilt_bdp_ppda <- list(
  "max_tilt" = tilt_bdp_ppda$team[tilt_bdp_ppda$tilt == max(tilt_bdp_ppda$tilt)],
  "min_tilt" = tilt_bdp_ppda$team[tilt_bdp_ppda$tilt == min(tilt_bdp_ppda$tilt)],
  "max_ppda" = tilt_bdp_ppda$team[tilt_bdp_ppda$ppda == max(tilt_bdp_ppda$ppda)],
  "min_ppda" = tilt_bdp_ppda$team[tilt_bdp_ppda$ppda == min(tilt_bdp_ppda$ppda)],
  "max_bdp" = tilt_bdp_ppda$team[tilt_bdp_ppda$build_up_disruption == max(tilt_bdp_ppda$build_up_disruption)],
  "min_bdp" = tilt_bdp_ppda$team[tilt_bdp_ppda$build_up_disruption == min(tilt_bdp_ppda$build_up_disruption)]
)
summary_path <- glue::glue("/workdir/results/summary_tilt_bdp_ppda_{league}.json")
max_min_tilt_bdp_ppda |>
  jsonlite::toJSON(auto_unbox = TRUE) %>%
  jsonlite::prettify() |>
  write(summary_path)