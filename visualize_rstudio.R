# Visualization of comparison results in RStudio
print("🔹 Visualizing comparison results in RStudio...")

# Define columns for DIAMOND data
diamondCol <- c("qseqid", "sseqid", "pident", "length", "mismatch",
                "gapopen", "qstart", "qend", "sstart", "send",
                "evalue", "bitscore", "qlen", "qseq", "stitle",
                "slen", "sseq")

# Get command line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 2) {
  stop("Usage: Rscript visualize_rstudio.R <data_folder> <max_length>")
}

data_folder <- args[1]  # Subfolder name or "all"
max_length_input <- args[2]  # Maximum peptide length or "auto"

# Check if folder name was provided
if (data_folder == "") {
  stop("No folder name provided. Please run the script again with a folder name.")
}

# Set path to results folder
main_path <- file.path(Sys.getenv("HOME"), "Desktop", "Databases_analysis_diamond", "Comparison_results")
print(paste("Results folder path:", main_path))

if (data_folder == "all") {
  selected_folders <- list.dirs(main_path, full.names = TRUE, recursive = FALSE)
} else {
  selected_path <- file.path(main_path, data_folder)
  if (!dir.exists(selected_path)) {
    stop(paste("Folder", selected_path, "does not exist. Please check the name and try again."))
  }
  selected_folders <- selected_path
}

# Check if maximum length should be auto-adjusted
auto_adjust <- (max_length_input == "auto")
if (!auto_adjust) {
  max_length <- as.numeric(max_length_input)
  if (is.na(max_length) || max_length <= 0) {
    stop("Invalid maximum length value. Please run the script again with a valid value.")
  }
} else {
  max_length <- NULL
}

# Process data and create visualizations
library(tidyverse)
library(ggplot2)

for (folder in selected_folders) {
  files <- list.files(folder, pattern = "_diamond.tsv$")
  databases <- unique(sub("^.*_(.*?)_diamond\\.tsv$", "\\1", files))
  
  for (i in 1:length(databases)) {
    for (j in 1:length(databases)) {
      db1 <- databases[i]
      db2 <- databases[j]
      
      file1 <- file.path(folder, paste0(db1, "_", db2, "_diamond.tsv"))
      file2 <- file.path(folder, paste0(db1, "_", db1, "_diamond.tsv"))
      
      if (file.exists(file1) & file.exists(file2)) {
        print(paste("Processing files:", file1, "and", file2))
        
        data1 <- read_tsv(file1, col_names = diamondCol, skip = 1)
        data2 <- read_tsv(file2, col_names = diamondCol, skip = 1)

        if (nrow(data1) == 0) {
          print(paste("No data in file:", file1))
          next
        }

        prepare_data <- function(data) {
          data %>%
            separate(qseqid, c("qid", "qname1"), "\\|", fill = "right") %>%
            separate(stitle, c("sseq", "sid", "sname"), "\\|", fill = "right") %>%
            separate(sname, c("sname1", "sname2"), "\\s", extra = "merge")
        }
        
        data1_id <- prepare_data(data1)
        data2_id <- prepare_data(data2)
        
        if (auto_adjust) {
          max_length <- max(data1_id$length, na.rm = TRUE)
        }
        
        output_folder <- file.path(Sys.getenv("HOME"), "Desktop", "Databases_analysis_diamond", "R", db1)
        if (!dir.exists(output_folder)) {
          dir.create(output_folder, recursive = TRUE)
        }
        
        # Create histogram plot
        hist_plot <- ggplot() +
          geom_histogram(data = data2_id, aes(pident, fill = "reference_db1"), binwidth = 2, color = "black", alpha = 0.5) +
          geom_histogram(data = data1_id, aes(pident, fill = "db1_vs_db2"), binwidth = 2, color = "black", alpha = 0.5) +
          labs(title = paste("Histogram comparison of", db1, "vs", db2),
               x = "[% identity]",
               y = "[Hits count]") +
          scale_fill_manual(values = c("db1_vs_db2" = "blue", "reference_db1" = "gray"),
                            labels = c(paste(db1, "vs", db2), paste("Reference Database", db1))) +
          theme(legend.title = element_blank()) +
          theme(plot.margin = margin(10, 10, 10, 10))

        hist_file <- paste0(db1, "_vs_", db2, "_histogram", if (!is.null(max_length)) paste0("_", max_length))
        ggsave(file.path(output_folder, paste0(hist_file, ".png")),
               plot = hist_plot,
               device = "png",
               dpi = 300,
               width = 10, height = 8)
        
        # Create scatter plot
        scatter_plot <- ggplot() +
          geom_count(data = data2_id, aes(length, pident, color = "reference_db1"), alpha = 0.5) +
          geom_count(data = data1_id, aes(length, pident, color = "db1_vs_db2"), alpha = 0.5) +
          labs(title = paste("AMPs distribution comparison between", db1, "and", db2),
               x = "[AMPs length]",
               y = "[% identity]") +
          scale_color_manual(values = c("db1_vs_db2" = "blue", "reference_db1" = "gray"),
                             labels = c(paste(db1, "vs", db2), paste("Reference Database", db1))) +
          theme(legend.title = element_blank()) +
          theme(plot.margin = margin(10, 10, 10, 10))

        if (!is.null(max_length)) {
          scatter_plot <- scatter_plot +
            scale_x_continuous(limits = c(0, max_length))
        }
        
        scatter_file <- paste0(db1, "_vs_", db2, "_scatter", if (!is.null(max_length)) paste0("_", max_length))
        ggsave(file.path(output_folder, paste0(scatter_file, ".png")),
               plot = scatter_plot,
               device = "png",
               dpi = 300,
               width = 10, height = 8)
      }
    }
  }
}
print("Results have been saved in the 'R' subfolder")
