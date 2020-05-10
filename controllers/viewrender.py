from datetime import datetime as dt
import sys
import traceback

class HtmlRender():
    """
    テーブルを描画して返す
    """
    def __init__(self,data=None):
        self.data = data
    def tablerender(self,data):
        try:
            t = self.get_title(data)
            ohtml = self.make_html(t,data)
            return ohtml
        except Exception as e:
            print('Error TableRendermain' )
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def get_title(self,data):
        try:
            keys = []
            for i,rs in enumerate(data):
                if type(rs) is str:
                   rs = dict(data)                 
                if i == 0:
                    keys = [ j for j in rs.keys()]
                else:
                    break
            return keys
        except Exception as e:
            print('Error get_title')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def make_html(self,titles,data):
        try:
            body = """
            <div id = content>
            <style type="text/css">
                    th, td {
                            width: 100px ;
                    }
                    thead, tbody {
                    display: block;
                    }
                    tbody {
                    overflow-x: hidden;
                    overflow-y: scroll;
                    height: 600px;
                    }
            </style>
            <table border=1>
                    <thead>
                        <tr>
            """
            flg = 0
            for t in titles:
                if t != 'etag':
                    body += '<th>' + t + '</th>'
            body += '</tr></thead>'
            body += '<tbody>'
            for r in data:
                if type(r) is str:
                   r = dict(data)
                   flg = 1
                body += '<tr>'
                for k in titles:
                    if k != 'etag':
                        if type(r[k]) is str:
                            body += '<td>' + r[k] + '</td>'
                        elif isinstance(r[k],dt):
                            v = r[k].strftime('%Y-%m-%d %H:%M:%S')
                            body += '<td>' + v + '</td>'
                        else:
                            body += '<td>－</td>'
                body += '</tr>'
                if flg == 1 :
                   break
            body += """
                    </tbody>
                </table>
                </div>
                """   
            return body
        except Exception as e:
            print('Error Render')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False
    def make_selectbox(self,data,name):
        try:
            body = '<select name = "table_name">'
            for sb in data:
                if name == sb:
                   body += '<option value="' + sb + '" selected >' + sb +'</option>'
                else:
                   body += '<option value="' + sb + '">' + sb +'</option>'
            body += '</select>'
            return body
        except Exception as e:
            print('Error get_title')
            t, v, tb = sys.exc_info()
            print(traceback.format_exception(t,v,tb))
            print(traceback.format_tb(e.__traceback__))
            return False

