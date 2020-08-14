import turbo_dash

# grab our data
df = turbo_dash.data.gapminder()

# Here's where all the magic happens. This creates our dashboard.
turbo_dashboard = turbo_dash.turbo_dashboard(
    # template
    template='turbo-dark',

    # dashboard pages
    dashboard_page_list=[
        # App 1
        turbo_dash.turbo_dashboard_page(
            # page information
            url='/app1',
            name='App 1',

            # data
            df=df,  # setting our data at the page level allows us to use different datasets for each page

            # menu filters, i.e. dropdown, slider, etc
            menu_filter_list=[
                turbo_dash.turbo_filter(filter_type='Dropdown-multi', column='country'),
                turbo_dash.turbo_filter(filter_type='RangeSlider', column='year'),
            ],

            # outputs, i.e. graphs, images, etc
            output_list=[
                # bar graph of population vs year
                turbo_dash.turbo_output(
                    output_type='bar',
                    x='year',
                    y='pop',
                    color='continent',
                    hover_name='country',
                    output_name='Population over time',
                ),

                # line graph of life expectancy vs year with an input to change the y axis to a different column
                turbo_dash.turbo_output(
                    output_type='line',
                    x='year',
                    y='lifeExp',
                    color='country',
                    chart_input_list=['y'],
                ),
            ],
        ),

        # App 2
        turbo_dash.turbo_dashboard_page(
            # page information
            url='/app2',
            name='App 2',

            # data
            df=df,  # setting our data at the page level allows us to use different datasets for each page

            # menu filters, i.e. dropdown, slider, etc
            menu_filter_list=[
                turbo_dash.turbo_filter(filter_type='Checklist', column='continent'),
            ],

            # outputs, i.e. graphs, images, etc
            output_list=[
                # line graph of gdpPercap vs year
                turbo_dash.turbo_output(
                    output_type='line',
                    x='year',
                    y='gdpPercap',
                    color='country',
                ),
            ],
        ),

        # Playground
        turbo_dash.turbo_dashboard_page(
            # page information
            url='/playground',
            name='Playground',

            # data
            df=df,  # setting our data at the page level allows us to use different datasets for each page

            # menu filters, i.e. dropdown, slider, etc
            menu_filter_list=[
                turbo_dash.turbo_filter(filter_type='Checklist', column='continent'),
                turbo_dash.turbo_filter(filter_type='Dropdown-multi', column='country'),
                turbo_dash.turbo_filter(filter_type='RangeSlider', column='year'),
            ],

            # outputs, i.e. graphs, images, etc
            output_list=[
                # line graph of gdpPercap vs year
                turbo_dash.turbo_output(
                    output_type='line',
                    x='year',
                    y='gdpPercap',
                    color='country',
                    chart_input_list=[
                        'output_type',
                        'x',
                        'y',
                        'z',
                        'color',
                        'size',
                        'hover_name',
                        'hover_data',
                        'locations',
                        'locationmode',
                        'projection',
                    ],
                ),
            ],
        ),

    ],
)

# Execute the code in a development environment. For deploying in production, see the "Deploying in Production"
#   section of the README here: https://github.com/turbo3136/turbo_dash/blob/master/README.md
if __name__ == '__main__':
    server = turbo_dashboard.run_dashboard(app_name=__name__)
