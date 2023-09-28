import dash

def register_callbacks(app):

    @app.callback(
        [dash.dependencies.Output('section1', 'style'),
         dash.dependencies.Output('section2', 'style')],
        [dash.dependencies.Input('btn-section1', 'n_clicks'),
         dash.dependencies.Input('btn-section2', 'n_clicks')]
    )
    def toggle_sections(btn1, btn2):
        ctx = dash.callback_context
        if not ctx.triggered:
            return dict(), {'display': 'none'}
        else:
            btn_id = ctx.triggered[0]['prop_id'].split('.')[0]
            if btn_id == 'btn-section1':
                return {'display': 'block'}, {'display': 'none'}
            elif btn_id == 'btn-section2':
                return {'display': 'none'}, {'display': 'block'}
