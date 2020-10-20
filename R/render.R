library(rmarkdown)

print("Render summary")

#Called directly when using subprocess interface
#grid_cells <- file('stdin')
#open(grid_cells)
#grid_cell_indices <- readLines(grid_cells, n=1)
#grid_cell_indices <- strsplit(grid_cell_indices, ',')
#grid_cell_indices <- unlist(lapply(grid_cell_indices, FUN=strtoi))
#render('summary.Rmd', params=list("indices"=grid_cell_indices), output_dir="R/summary")

#rpy2 likes to have a function to call
render_summary <- function(grid_cells)
{
	render('R/summary.Rmd', params=list("indices"=grid_cells), output_dir="R/summary")
}