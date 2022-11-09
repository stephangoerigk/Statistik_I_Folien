#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Trajectory Viewer"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            sliderInput("i1",
                        "Intercept:",
                        min = 0,
                        max = 50,
                        value = 25),
            sliderInput("b1",
                        "b1:",
                        min = -10,
                        max = 10,
                        step = 0.01,
                        value = 0),
            sliderInput("b2",
                        "b2:",
                        min = -10,
                        max = 10,
                        step = 0.01,
                        value = 0),
            sliderInput("b3",
                        "b3:",
                        min = -10,
                        max = 10,
                        step = 0.01,
                        value = 0)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("distPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    #+ rnorm(nrow(df), 0, 3)
    
    n <- 1 #number of individuals
    t <- 1:10   #number of time periods
    dat <- expand.grid(t=1:t,id=1:n)
    df = data.frame(t = rep(t, n))
    
    output$distPlot <- renderPlot({
        
        df$y_1 = input$i1 + input$b1*t 
        df$y_2 = input$i1 + input$b1*t + input$b2*t^2 
        df$y_3 = input$i1 + input$b1*t + input$b2*t^2 + input$b3*t^3 
        
        cowplot::plot_grid(ggplot(data = df, aes(x = t, y = y_1)) +
                               geom_point() +
                               labs(y = "y", x = "Time") +
                               coord_cartesian(ylim = c(-50,50)) +
                               theme_classic(),
                           ggplot(data = df, aes(x = t, y = y_2)) +
                               geom_point() +
                               labs(y = "y", x = "Time") +
                               coord_cartesian(ylim = c(-50,50)) +
                               theme_classic(),
                           ggplot(data = df, aes(x = t, y = y_3)) +
                               geom_point() +
                               labs(y = "y", x = "Time") +                            
                               coord_cartesian(ylim = c(-50,50)) +
                               theme_classic(), ncol = 3, labels = c("Linear", "Quadratic", "Cubic"))
        
    })
}

# Run the application 
shinyApp(ui = ui, server = server)
