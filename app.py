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
