#!/usr/local/bin/Rscript

app_data <- read.csv('./data.csv', sep = ";", header=TRUE);

app_data$sablona[app_data$pouzita_sablona == "True"] <- "ANO"
app_data$sablona[app_data$pouzita_sablona == "False"] <- "NE"
app_data$titul[app_data$vs_titul == "True"] <- "ANO"
app_data$titul[app_data$vs_titul == "False"] <- "NE"

# software/šablona
table1 <- table(app_data$software, app_data$sablona, dnn=c("Software", "Použita šablona"));

# vš/šablona
table2 <- table(app_data$titul, app_data$sablona, dnn=c("VŠ titul", "Použita šablona"));

addmargins(table1);
addmargins(table2);

# export do SVG
svg("data_2022.svg", width = 9, height = 4.5);
par(mfrow = c(1, 2));

# barvy
bar_col = c("turquoise4", "turquoise3", "turquoise2", "turquoise");

barplot(table1,
	ylab="Celkový počet APP",
	xlab="Použita naše šablona",
	main="Software a šablony",
	col=bar_col,
	beside <- FALSE, xlim=c(0,1), width=.3
)
legend(
	"topright",
	title = "Software",
	legend = sort(unique(app_data$software)),
	fill = bar_col,
	box.lty=0
)

barplot(table2,
	ylab="Celkový počet APP",
	xlab="Použita naše šablona",
	main="Předchozí VŠ titul",
	col=bar_col,
	beside <- FALSE, xlim=c(0,1), width=.3
)
legend(
	"topright",
	title = "VŠ titul",
	legend = sort(unique(app_data$titul)),
	fill = bar_col,
	box.lty=0
)

par(mfrow = c(1, 1));
dev.off();