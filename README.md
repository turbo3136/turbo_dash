# turbo_dash
automated Dash framework with templates

## Quickstart
`pip install turbo-dash`

## Goal
The goal of the `turbo_dash` project is to create a wrapper for [plotly dash](https://plotly.com/dash/) that allows an 
inexperienced python developer to quickly create a simple, clean, interactive, easy to manipulate dashboard.

## OKRs
<table>
    <tbody>
        <tr>
            <th>Objectives</th>
            <th>Key Results</th>
            <th>Status</th>
        </tr>
        <tr>
            <td rowspan="3">
                1. `turbo_dash` requires minimal python, plotly, or dash knowledge to create a fully functional 
                dashboard, as measured by:
            </td>
            <td>i. less than 10 lines of code required per object</td>
            <td>:white-circle:</td>
        </tr>
        <tr>
            <td>ii. full documentation with examples for every developer-facing object</td>
            <td>:white-circle:</td>
        </tr>
        <tr>
            <td>iii. a suite of user-friendly templates that design the layout for the developer</td>
            <td>:white-circle:</td>
        </tr>
        <tr>
            <td>
                2. `turbo_dash` executes commands quickly and displays minimal lag between 
                input and output, as measured by:
            </td>
            <td>i. less than 1s load times for datasets up to 1M rows on a standard laptop CPU</td>
            <td>:white-circle:</td>
        </tr>
        <tr>
            <td>3. `turbo_dash` doesn't break, as measured by:</td>
            <td>i. comprehensive test suite</td>
            <td><span style="color: grey; font-size: 40px;">&#9210;</span></td>
        </tr>
    </tbody>
</table>

## Example minimalist app
`app.py`
```
import turbo_dash

# grab our data
df = turbo_dash.data.gapminder()

# Here's where all the magic happens. This creates our dashboard.
turbo_dashboard = turbo_dash.dashboard(
    # template
    template='turbo',

    # dashboard pages
    dashboard_page_list=[
        # App 1
        turbo_dash.dashboard_page(
            # page information
            url='/app1',
            name='App 1',

            # data
            df=df,  # setting our data at the page level allows us to use different datasets for each page

            # menu, i.e. sidebar with filters
            menu=turbo_dash.turbo_menu(
                df=df,
                filter_list=[
                    turbo_dash.turbo_filter(type='Dropdown', column='country'),
                    turbo_dash.turbo_filter(type='RangeSlider', column='year'),
                ],
            ),

            # content, i.e. graphs, images, etc
            content=turbo_dash.turbo_content(
                df=df,
                output_list=[
                    # bar graph of population vs year
                    turbo_dash.turbo_output(type='bar', x='year', y='pop'),

                    # line graph of life expectancy vs year with an input to change the y axis to a different column
                    turbo_dash.turbo_output(
                        type='line',
                        x='year',
                        y='lifeExp',
                        input_list=['y'],
                    ),
                ],
            ),
        ),

        # App 2
        turbo_dash.dashboard_page(
            # page information
            url='/app2',
            name='App 2',

            # data
            df=df,  # setting our data at the page level allows us to use different datasets for each page

            # menu, i.e. sidebar with filters
            menu=turbo_dash.turbo_menu(
                df=df,
                filter_list=[
                    turbo_dash.turbo_filter(type='Checklist', column='continent'),
                ],
            ),

            # content, i.e. graphs, images, etc
            content=turbo_dash.turbo_content(
                df=df,
                output_list=[
                    # line graph of gdpPercap vs year
                    turbo_dash.turbo_output(type='line', x='year', y='gdpPercap'),
                ],
            ),
        ),

    ],
)

# execute the code
if __name__ == '__main__':
    turbo_dashboard.run_dashboard()
```
