import turbo_dash

# grab our data
df = turbo_dash.data.gapminder()

# Here's where all the magic happens. This creates our dashboard.
turbo_dashboard = turbo_dash.turbo_dashboard(
    # template
    template='turbo',

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

    ],
)

# execute the code
if __name__ == '__main__':
    turbo_dashboard.run_dashboard(app_name=__name__)
