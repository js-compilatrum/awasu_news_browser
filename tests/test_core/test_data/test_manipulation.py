from core.data.manipulation import get_all_channels
from core.data.manipulation import find_channels

folders = {'channelFolder': {'id': '50793385-7890-405F-9D04-367D4D27F85A', 'name': 'International',
                             'channelFolders': [{'channelFolder': {'id': '52231ADB-3DE0-4E54-B80C-9C8B63A81884',
                                                                   'name': 'World', 'channelFolders': [{
                                                                                                           'channelFolder': {
                                                                                                               'id': 'C819096D-2713-4600-A7F4-BAF39E3FC8A3',
                                                                                                               'name': 'News International Agency',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': '3DAE8D17-ABAD-4193-9DB9-55E8F3703202',
                                                                                                               'name': 'News Agregators',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': 'F331A052-9EF4-47EE-934E-1938EE29E252',
                                                                                                               'name': 'S.E. Asia',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': 'C2BB8478-1FD4-4289-AB8B-E2850303BA7B',
                                                                                                               'name': 'Africa',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': '083D3279-819A-487B-A3B7-1C2334939232',
                                                                                                               'name': 'Sydney Morning Herald',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': 'E45AA385-B071-4575-853A-BCA97222B89E',
                                                                                                               'name': 'International Herald Tribune',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': 'F1323EB1-A285-4EB5-A574-D6B86AE69D4F',
                                                                                                               'name': 'Washington Post',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': 'C4304EF0-2D7C-4E99-A350-2E414BA5EBCE',
                                                                                                               'name': 'The Guardian',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': '15802F07-7D3A-42B8-833C-17130E3B10CB',
                                                                                                               'name': 'The New York Times',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': '766DAA7C-0825-4762-B2D4-AFFAB1742532',
                                                                                                               'name': 'BBC',
                                                                                                               'channelFolders': []}},
                                                                                                       {
                                                                                                           'channelFolder': {
                                                                                                               'id': '83A40923-2B4D-4CF4-AF5B-526D54865F20',
                                                                                                               'name': 'The Age',
                                                                                                               'channelFolders': []}}]}},
                                                {'channelFolder': {'id': '2A551C69-E584-4C7F-8BB5-C5B75682DD52',
                                                                   'name': 'Religion', 'channelFolders': [{
                                                                                                              'channelFolder': {
                                                                                                                  'id': '27CE69E3-17B6-41BE-AD0B-2081ACD9CAFF',
                                                                                                                  'name': 'Jewish',
                                                                                                                  'channelFolders': []}},
                                                                                                          {
                                                                                                              'channelFolder': {
                                                                                                                  'id': '7EAB7D37-2703-4BF9-8629-998F78502508',
                                                                                                                  'name': 'Islamic',
                                                                                                                  'channelFolders': []}}]}},
                                                {'channelFolder': {'id': '4E6ED13F-E5E6-45AB-8082-A68083CF2D96',
                                                                   'name': 'Continents', 'channelFolders': [{
                                                                                                                'channelFolder': {
                                                                                                                    'id': 'DBB0F629-C0DF-4583-845F-BF84987029CF',
                                                                                                                    'name': 'North America',
                                                                                                                    'channelFolders': [
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': 'AF47436B-F7FA-4942-AFD6-9F1777A08202',
                                                                                                                                'name': 'USA',
                                                                                                                                'channelFolders': [
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': '8FA52DD2-577D-427C-B6AB-1BA0633CB6CE',
                                                                                                                                            'name': 'New York Time',
                                                                                                                                            'channelFolders': []}},
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': 'B57349F6-CDEE-41DC-A8D6-552736D7615F',
                                                                                                                                            'name': 'Financial Times',
                                                                                                                                            'channelFolders': []}},
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': '96128568-219F-4E72-8D1D-5CFD51202EE8',
                                                                                                                                            'name': 'Economist',
                                                                                                                                            'channelFolders': []}},
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': 'BFF11A51-AE99-4770-B9BE-6C875A73A2F2',
                                                                                                                                            'name': 'yahoo',
                                                                                                                                            'channelFolders': []}},
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': 'AE3CEC09-E8E8-4C1D-9177-BC03E6FEA6F3',
                                                                                                                                            'name': 'san diego',
                                                                                                                                            'channelFolders': []}},
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': 'C6541FE3-0186-49BB-A823-73F85702212D',
                                                                                                                                            'name': 'USA News Firehose',
                                                                                                                                            'channelFolders': []}}]}}]}},
                                                                                                            {
                                                                                                                'channelFolder': {
                                                                                                                    'id': '089E383F-456C-4761-BE23-A9BA0A86E3C6',
                                                                                                                    'name': 'Europe',
                                                                                                                    'channelFolders': [
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': 'CDD2549B-9B9B-4FEA-B36A-15948D017BA9',
                                                                                                                                'name': 'Germany',
                                                                                                                                'channelFolders': []}},
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': '8A1C49D1-0FAC-4141-9D1F-1325CC47D6D6',
                                                                                                                                'name': 'GB',
                                                                                                                                'channelFolders': [
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': '79EAF436-803A-4E06-B43A-E6ED78A115B0',
                                                                                                                                            'name': 'BBC',
                                                                                                                                            'channelFolders': []}}]}},
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': '8201D81B-CEC1-4622-B686-4BE57C325238',
                                                                                                                                'name': 'France',
                                                                                                                                'channelFolders': []}}]}},
                                                                                                            {
                                                                                                                'channelFolder': {
                                                                                                                    'id': '5913D2DD-D55C-4CD0-A89C-DB126F26BFD0',
                                                                                                                    'name': 'Australia',
                                                                                                                    'channelFolders': []}},
                                                                                                            {
                                                                                                                'channelFolder': {
                                                                                                                    'id': '7E72A345-9353-4699-B3FE-E095B4CC9E36',
                                                                                                                    'name': 'Asia',
                                                                                                                    'channelFolders': [
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': '7EA3C074-C2E2-42A9-83AD-058F70BE0DDE',
                                                                                                                                'name': 'Russia',
                                                                                                                                'channelFolders': []}},
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': '436B19F7-60FC-44FD-BC1E-527D46552808',
                                                                                                                                'name': 'Japan',
                                                                                                                                'channelFolders': []}},
                                                                                                                        {
                                                                                                                            'channelFolder': {
                                                                                                                                'id': '849CE798-D324-401C-88C8-7F8D204EA4FF',
                                                                                                                                'name': 'China',
                                                                                                                                'channelFolders': [
                                                                                                                                    {
                                                                                                                                        'channelFolder': {
                                                                                                                                            'id': '5D93371C-6FCA-44B5-A880-3619DAD5C8FD',
                                                                                                                                            'name': 'Xinhuanews',
                                                                                                                                            'channelFolders': []}}]}}]}}]}},
                                                {'channelFolder': {'id': '36D3266F-9B81-43D3-B9F1-3BFD9CECE428',
                                                                   'name': 'China', 'channelFolders': []}}, {
                                                    'channelFolder': {'id': '6225AB49-31CE-492B-A272-21D742B155FE',
                                                                      'name': 'Reuters', 'channelFolders': []}}]}}

flattened = {'International': '50793385-7890-405F-9D04-367D4D27F85A', 'World': '52231ADB-3DE0-4E54-B80C-9C8B63A81884',
             'News International Agency': 'C819096D-2713-4600-A7F4-BAF39E3FC8A3',
             'News Agregators': '3DAE8D17-ABAD-4193-9DB9-55E8F3703202',
             'S.E. Asia': 'F331A052-9EF4-47EE-934E-1938EE29E252', 'Africa': 'C2BB8478-1FD4-4289-AB8B-E2850303BA7B',
             'Sydney Morning Herald': '083D3279-819A-487B-A3B7-1C2334939232',
             'International Herald Tribune': 'E45AA385-B071-4575-853A-BCA97222B89E',
             'Washington Post': 'F1323EB1-A285-4EB5-A574-D6B86AE69D4F',
             'The Guardian': 'C4304EF0-2D7C-4E99-A350-2E414BA5EBCE',
             'The New York Times': '15802F07-7D3A-42B8-833C-17130E3B10CB',
             'BBC': '79EAF436-803A-4E06-B43A-E6ED78A115B0', 'The Age': '83A40923-2B4D-4CF4-AF5B-526D54865F20',
             'Religion': '2A551C69-E584-4C7F-8BB5-C5B75682DD52', 'Jewish': '27CE69E3-17B6-41BE-AD0B-2081ACD9CAFF',
             'Islamic': '7EAB7D37-2703-4BF9-8629-998F78502508', 'Continents': '4E6ED13F-E5E6-45AB-8082-A68083CF2D96',
             'North America': 'DBB0F629-C0DF-4583-845F-BF84987029CF', 'USA': 'AF47436B-F7FA-4942-AFD6-9F1777A08202',
             'New York Time': '8FA52DD2-577D-427C-B6AB-1BA0633CB6CE',
             'Financial Times': 'B57349F6-CDEE-41DC-A8D6-552736D7615F',
             'Economist': '96128568-219F-4E72-8D1D-5CFD51202EE8', 'yahoo': 'BFF11A51-AE99-4770-B9BE-6C875A73A2F2',
             'san diego': 'AE3CEC09-E8E8-4C1D-9177-BC03E6FEA6F3',
             'USA News Firehose': 'C6541FE3-0186-49BB-A823-73F85702212D',
             'Europe': '089E383F-456C-4761-BE23-A9BA0A86E3C6', 'Germany': 'CDD2549B-9B9B-4FEA-B36A-15948D017BA9',
             'GB': '8A1C49D1-0FAC-4141-9D1F-1325CC47D6D6', 'France': '8201D81B-CEC1-4622-B686-4BE57C325238',
             'Australia': '5913D2DD-D55C-4CD0-A89C-DB126F26BFD0', 'Asia': '7E72A345-9353-4699-B3FE-E095B4CC9E36',
             'Russia': '7EA3C074-C2E2-42A9-83AD-058F70BE0DDE', 'Japan': '436B19F7-60FC-44FD-BC1E-527D46552808',
             'China': '36D3266F-9B81-43D3-B9F1-3BFD9CECE428', 'Xinhuanews': '5D93371C-6FCA-44B5-A880-3619DAD5C8FD',
             'Reuters': '6225AB49-31CE-492B-A272-21D742B155FE'}


def test_get_all_channels():
    assert get_all_channels(folders) == flattened
    assert len(get_all_channels(folders)) == len(flattened)


def test_find_channels():
    assert len(find_channels(folders, 'World')) == 11  # number of subfolder
    assert find_channels(folders, 'No Exist folder') == False
