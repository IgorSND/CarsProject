library(shiny)
library(tibble)
library(dplyr)

# Definir média e desvio padrão da quilometragem a partir dos dados de treinamento
mileage_mean <- 106922.3
mileage_sd <- 46797.29

final_coefs <- tibble(
  term = c("(Intercept)", "mileage", "vehicle_brand_Fiat", "vehicle_brand_Ford", "vehicle_brand_GM_Chevrolet", "vehicle_brand_Honda", "vehicle_brand_Hyundai", 
           "vehicle_brand_Jeep", "vehicle_brand_other", "vehicle_brand_Peugeot", "vehicle_brand_Renault", "vehicle_brand_Toyota", "vehicle_brand_VW_Volkswagen",
           "car_type_other", "car_type_Pick_up", "car_type_Sedan", "car_type_SUV", "car_type_Van", "registration_year_X2008", "registration_year_X2009", 
           "registration_year_X2010", "registration_year_X2011", "registration_year_X2012", "registration_year_X2013", "registration_year_X2014", 
           "registration_year_X2015", "registration_year_X2016", "registration_year_X2017", "registration_year_X2018", "registration_year_X2019", 
           "registration_year_X2020", "registration_year_X2021", "registration_year_X2022", "registration_year_other", "engine_power_X1.3", 
           "engine_power_X1.4", "engine_power_X1.5", "engine_power_X1.6", "engine_power_X1.8", "engine_power_X2", "engine_power_other", 
           "steering_type_Hydraulic", "steering_type_Mechanical", "steering_type_other", "number_of_doors_X4", "tax_status_Yes"),
  estimate = c(56304, -2670, 990, 1110, 3356, 5874, 2908, 2482, 6779, 97.1, 351, 4766, 3725, 1147, 5051, 2429, 4884, 2034, 250, 233, 1286, 2464, 3811, 5723, 
               5856, 5549, 6634, 8025, 8352, 7658, 9194, 10949, 10545, -1047, 915, 3256, -57.5, 2717, 3283, 7728, 228, -3383, -893, -128, 2522, -11.5)
)

ui <- fluidPage(
  tags$head(
    tags$link(rel = "stylesheet", type = "text/css", href = "estilo.css")
  ),
  
  div(class = "header-container"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("vehicle_brand", "Vehicle Brand", choices = c("Citroën", "Fiat", "Ford", "GM - Chevrolet", "Honda", "Hyundai", "Jeep", "Other", "Peugeot", "Renault", "Toyota", "VW - Volkswagen")),
      selectInput("car_type", "Car Type", choices = c("Hatchback", "Other", "Pick-up", "Sedan", "SUV", "Van")),
      selectInput("registration_year", "Registration Year", choices = c(as.character(2008:2023), "other")),
      selectInput("engine_power", "Engine Power", choices = c("1.0", "1.3", "1.4", "1.5", "1.6", "1.8", "2.0", "Other")),
      selectInput("steering_type", "Steering Type", choices = c("Electric", "Hydraulic", "Mechanical", "Other")),
      selectInput("number_of_doors", "Number of Doors", choices = c("2", "4")),
      selectInput("tax_status", "Tax Status", choices = c("No", "Yes")),
      numericInput("mileage", "Mileage", value = 0, min = 0),
      actionButton("predict_button", "Predict Price")
    ),
    
    mainPanel(
      div(class = "content-box",
        div(class = "predicted-price", textOutput("predicted_price")))
    )
  )
)

# Definir server
server <- function(input, output) {
  
  predicted_price <- eventReactive(input$predict_button, {
    intercept <- final_coefs |>  filter(term == "(Intercept)") |>  pull(estimate)
    predicted_price <- intercept
    
    mileage_standardized <- (input$mileage - mileage_mean) / mileage_sd
    mileage_coef <- final_coefs |>  filter(term == "mileage") |>  pull(estimate)
    predicted_price <- predicted_price + mileage_coef * mileage_standardized
    
    user_data <- tibble(
      vehicle_brand_Fiat = ifelse(input$vehicle_brand == "Fiat", 1, 0),
      vehicle_brand_Ford = ifelse(input$vehicle_brand == "Ford", 1, 0),
      vehicle_brand_GM_Chevrolet = ifelse(input$vehicle_brand == "GM - Chevrolet", 1, 0),
      vehicle_brand_Honda = ifelse(input$vehicle_brand == "Honda", 1, 0),
      vehicle_brand_Hyundai = ifelse(input$vehicle_brand == "Hyundai", 1, 0),
      vehicle_brand_Jeep = ifelse(input$vehicle_brand == "Jeep", 1, 0),
      vehicle_brand_other = ifelse(input$vehicle_brand == "Other", 1, 0),
      vehicle_brand_Peugeot = ifelse(input$vehicle_brand == "Peugeot", 1, 0),
      vehicle_brand_Renault = ifelse(input$vehicle_brand == "Renault", 1, 0),
      vehicle_brand_Toyota = ifelse(input$vehicle_brand == "Toyota", 1, 0),
      vehicle_brand_VW_Volkswagen = ifelse(input$vehicle_brand == "VW - Volkswagen", 1, 0),
      car_type_other = ifelse(input$car_type == "Other", 1, 0),
      car_type_Pick_up = ifelse(input$car_type == "Pick-up", 1, 0),
      car_type_Sedan = ifelse(input$car_type == "Sedan", 1, 0),
      car_type_SUV = ifelse(input$car_type == "SUV", 1, 0),
      car_type_Van = ifelse(input$car_type == "Van", 1, 0),
      registration_year_X2008 = ifelse(input$registration_year == "2008", 1, 0),
      registration_year_X2009 = ifelse(input$registration_year == "2009", 1, 0),
      registration_year_X2010 = ifelse(input$registration_year == "2010", 1, 0),
      registration_year_X2011 = ifelse(input$registration_year == "2011", 1, 0),
      registration_year_X2012 = ifelse(input$registration_year == "2012", 1, 0),
      registration_year_X2013 = ifelse(input$registration_year == "2013", 1, 0),
      registration_year_X2014 = ifelse(input$registration_year == "2014", 1, 0),
      registration_year_X2015 = ifelse(input$registration_year == "2015", 1, 0),
      registration_year_X2016 = ifelse(input$registration_year == "2016", 1, 0),
      registration_year_X2017 = ifelse(input$registration_year == "2017", 1, 0),
      registration_year_X2018 = ifelse(input$registration_year == "2018", 1, 0),
      registration_year_X2019 = ifelse(input$registration_year == "2019", 1, 0),
      registration_year_X2020 = ifelse(input$registration_year == "2020", 1, 0),
      registration_year_X2021 = ifelse(input$registration_year == "2021", 1, 0),
      registration_year_X2022 = ifelse(input$registration_year == "2022", 1, 0),
      registration_year_other = ifelse(input$registration_year == "other", 1, 0),
      engine_power_X1_3 = ifelse(input$engine_power == "1.3", 1, 0),
      engine_power_X1_4 = ifelse(input$engine_power == "1.4", 1, 0),
      engine_power_X1_5 = ifelse(input$engine_power == "1.5", 1, 0),
      engine_power_X1_6 = ifelse(input$engine_power == "1.6", 1, 0),
      engine_power_X1_8 = ifelse(input$engine_power == "1.8", 1, 0),
      engine_power_X2 = ifelse(input$engine_power == "2.0", 1, 0),
      engine_power_other = ifelse(input$engine_power == "Other", 1, 0),
      steering_type_Hydraulic = ifelse(input$steering_type == "Hydraulic", 1, 0),
      steering_type_Mechanical = ifelse(input$steering_type == "Mechanical", 1, 0),
      steering_type_other = ifelse(input$steering_type == "Other", 1, 0),
      number_of_doors_X4 = ifelse(input$number_of_doors == "4", 1, 0),
      tax_status_Yes = ifelse(input$tax_status == "Yes", 1, 0)
    )
    
    for (term in names(user_data)) {
      coef <- final_coefs |>  filter(term == !!term) |>  pull(estimate)
      if (length(coef) > 0) {
        predicted_price <- predicted_price + coef * user_data[[term]]
      }
    }
    
    return(predicted_price)
  })
  
  output$predicted_price <- renderText({
    price <- predicted_price()
    formatted_price <- formatC(price, format = "f", big.mark = ".", decimal.mark = ",", digits = 2)
    paste("Predicted Price: R$", formatted_price)
  })
  
}
shinyApp(ui = ui, server = server)
