import plotly.express as px
import dash
import dash_core_components as dcc


class TurboOutput:
    def __init__(
            self,
            output_component_id,
            output_component_property,
            output_type,
            df=None,
            x=None,
            y=None,
            color=None,
            template=None,
            turbo_input_list=None,
    ):
        """output object that will assemble the information we need

        :param output_component_id: component ID for the output, dash will use this in the callbacks
        :param output_component_property: property we want to update for the output, dash will use this in the callbacks
        :param output_type: string for the type of output we want to use,
            you might have to add functionality for your output if you're using a new one
        :param df: optional, dataframe we'll use to gather the output data
        :param x: optional, column we'll use for the x axis data
        :param y: optional, column we'll use for the y axis data
        :param color: optional, plotly express color argument (column to color accordingly)
        :param template: optional, plotly express template for the output
        :param turbo_input_list: optional, list of TurboInput objects that will affect this output
        """
        self.output_component_id = output_component_id
        self.output_component_property = output_component_property
        self.output_type = output_type
        self.df = df
        self.x = x
        self.y = y
        self.color = color
        self.template = template
        self.turbo_input_list = turbo_input_list

        # this is important! This is the dash output that the callback will update
        self.dash_dependencies_output = dash.dependencies.Output(
            component_id=self.output_component_id,
            component_property=self.output_component_property,
        )

        # this is also important! This is the list of dash inputs the callback will listen for
        # We need to flatten all the dash dependencies input lists for this output and grab the dependencies
        # this is using list comprehension, the expanded equivalent would be:
        # lst = []
        # for turbo_input in self.turbo_input_list:
        #     for item in turbo_input.dash_dependencies_input_list:
        #         lst.append(item)
        self.dash_dependencies_input_list = [
            inp for turbo_input in self.turbo_input_list for inp in turbo_input.dash_dependencies_input_list
        ]

        # yet again, this is important! We need to flatten all the input operator lists for this output.
        # We'll use the same method of list comprehension as above.
        self.input_operator_list = [
            operator for turbo_input in self.turbo_input_list for operator in turbo_input.input_operator_list
        ]

        # and again, this is important! We need to flatten all the input filter column lists
        # so we know which column to filter for each input
        self.input_filter_column_list = [
            col for turbo_input in self.turbo_input_list for col in turbo_input.input_filter_column_list
        ]

        self.html = dcc.Graph(id=self.output_component_id)  # set the html we'll use for the layout

    def assemble_output_object(self, filtered_df):
        """assemble the output object we want"""

        if self.output_type == 'bar':
            return px.bar(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'scatter':
            return px.scatter(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        elif self.output_type == 'line':
            return px.line(
                data_frame=filtered_df,
                x=self.x,
                y=self.y,
                color=self.color,
                template=self.template,
            )

        # who are you? who who, who who
        else:
            raise ValueError(
                """I don't know what to do with a "{}" output type. Please add it to {}."""
                .format(self.output_type, __file__)
            )

    def filter_dataframe(self, args):
        """filter the dataframe based on the input values, columns, and operators provided"""
        filtered_df = self.df

        for index, input_filter_value in enumerate(args):  # args is a list of all the filter input values

            # print(args)
            # print('index: {}, input_filter_value: {}'.format(index, input_filter_value))
            # print('operator: {}, column: {}'.format(self.input_operator_list[index], self.input_filter_column_list[index]))
            # print()

            if input_filter_value is not None:
                filtered_df = filtered_df[  # here we start the filtering, it's the "df[" part of "df[df['col'] == val]"
                    self.input_operator_list[index](  # now we grab our operator, something like operator.eq
                        filtered_df[self.input_filter_column_list[index]],  # pass the operator the dataframe's values
                        input_filter_value,  # and compare it to the filter input
                    )
                ]
                # okay, so. (you know it's gonna be complicated when you start a sentence with 'okay, so')
                # okay, so the filtering works by looking back at the operator we associated with this filter input
                # in the TurboFilter object. For example, the DatePickerRange has two inputs
                # one is 'start_date', the other 'end_date'. The operators are operator.ge and operator.le,
                # respectively. Those are the mathematical operators >=, <=, and they work like: operator.ge(2, 1)
                # returns True. So, we're filtering the df using the operator we found already
                # (self.input_operator_list[index]) using the column name associated with this filter
                # (self.input_filter_column_list[index]) and the input filter value as the arguments to the
                # mathematical operator. That filters our df as we want.

        # print(filtered_df.head())

        return filtered_df

    def callback(self, app_to_callback):
        @app_to_callback.callback(
            output=self.dash_dependencies_output,
            inputs=self.dash_dependencies_input_list,
        )
        def filter_and_assemble_output(*input_values):
            """put everything together into one function where we filter and assemble the output"""
            filtered_df = self.filter_dataframe(input_values)
            return self.assemble_output_object(filtered_df=filtered_df)
