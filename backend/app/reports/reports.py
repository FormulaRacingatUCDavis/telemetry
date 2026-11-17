def report_html(template, figs):
    """
    Interactive HTML report
    """
    plots = []
    for i, fig in enumerate(figs):
        plots.append(
            fig.to_html(
                full_html=False,
                include_plotlyjs=(i == 0),
                config={
                    "responsive": True,
                    "toImageButtonOptions": {
                        "format": "png",
                        "scale": 2
                    }
                }
            )
        )

    return template.render(plots=plots)