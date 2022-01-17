# Compartmental Model (Python 3.7)
### Epidemic simulation in a small virtual town

<br>

The user sets the value a number of parameters in order to extract statistics and deductions based on the behavior of the virtual residents.

![Graph](https://user-images.githubusercontent.com/25060780/149682101-7bc337ca-5cbc-47b2-93ab-d24a6f3e2138.png)

The program creates the virtual residents based on the given parameters. Each person has the following traits:
- Age (1 of 5 age groups)
- Health Factor: Determines the person's likelihood of being hospitalized during their infectious period.
- Hygiene Factor: Affects the person's likelihood to transmit and receive the virus.
- Legality Factor: Determines the person's likelihood to obey the "government's" protection measures during the pandemic.
- Daily routine: Defines the person's actions each day (in the morning children go to school, adults to work etc).

<br>

The simulation runs for the specified amount of weeks. The virtual residents "interact" with others throughout the day.
The population is divided into 3 compartments, depending on their state regarding to the virus:
- Susceptible
- Infectious
- Recovered

This kind of model is known as an **SIR Model**.
The user may choose not to include the "Recovered" state, which means that the people return to "Susceptible" after their infectious period. This is known as an **SIS Model**.

<br>

During the simulation, the virtual "government" sets protection measures in order to reduce cases. There are 3 emergency levels depending on the infectious percentage on the previous day.

<br>

As soon as the simulation is finished, a graph with the results is displayed.

![Results](https://user-images.githubusercontent.com/25060780/149684756-2840d9e8-80c6-4924-8960-df1e3a63d8d1.png)

The red line represents the percentage of Infectious people for each day, and the green line represents the Recovered.
The vertical dashed lines show the changes in the protection measures. The darker the color, the higher the emergency level.

<br>

There is also an option which allows the results to be displayed as an animated pie chart.

![Pie Chart](https://user-images.githubusercontent.com/25060780/149688012-4dc49d51-24c2-4df1-af16-884fe36b1a39.gif)

The chart is constantly updating, showing the changes among the 3 states throughout the simulation.

<br><br><br>
*Created in the context of my thesis (Papadimitriou Asterios, February 2022)*
