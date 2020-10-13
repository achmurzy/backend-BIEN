library(rmarkdown)

grid_cells <- file('stdin')
open(grid_cells)
grid_cell_indices <- readLines(grid_cells, n=1)
grid_cell_indices <- strsplit(grid_cell_indices, ',')
grid_cell_indices <- unlist(lapply(grid_cell_indices, FUN=strtoi))
#while(length(line <- readLines(grid_cells,n=1)) > 0) {
  # write(line, stderr())
#  print(line)
#}
render('summary.Rmd', params=list("indices"=grid_cell_indices), output_dir="summary")

render_summary <- function(grid_cells)
{
	render('summary.Rmd', params=list("indices"=grid_cells), output_dir="summary")
}