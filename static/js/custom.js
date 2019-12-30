let table = new Tabulator("#awasu-news-data", {
    height: "{{ articles_data|df_to_pxsize}}px",
    layout: "fitColumns",
    groupBy: "Channel",
    columns: [ //Define Table Columns
        {title: "Channel", field: "Channel", width: 150},
        {title: "Title", field: "Title"},
        {title: "Published", field: "Published"},
        {title: "Link", field: "Link", formatter: "link", formatterParams: {urlField: "Link", target: "_blank"}},
    ],
    rowClick(e, row) {
        var row_data = row.getData();
        console.log(row_data);
        let art_data = {
            'channel': row_data.Channel,
            'title': row_data.Title,
            'url': row_data.Link,
            'published': row_data.Published,
            'view': window.location.pathname
        };

        $.ajax({
            type: 'POST',
            url: '{{url_for("add_article")}}',
            contentType: 'application/json;charset=UTF-8',
            dataType: "json",
            data: JSON.stringify(art_data),
            success: function (response) {
                console.log(response);
                $(".infobox p").text('Last added: ' + response['info']);
            },
            error: function (error) {
                console.log(error);
            },
        });
    },

});