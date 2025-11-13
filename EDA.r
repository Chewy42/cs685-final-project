rand_sample <- read.csv("openalex_sample.csv")
upper_bound_sample <- read.csv("top_1000_papers.csv")

rand_sample$cited_by_count <- as.numeric(rand_sample$cited_by_count)
upper_bound_sample$cited_by_count <- as.numeric(upper_bound_sample$cited_by_count)

print(mean(rand_sample$cited_by_count))

print(mean(upper_bound_sample$cited_by_count))
