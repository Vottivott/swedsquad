from bs4 import BeautifulSoup

def strip_html_tags(html):
    return str(BeautifulSoup(html, 'html.parser').get_text())

def get_answers_and_answer_starts(html):
    answer_text = {}
    answer_start = {}
    answer_earliest = {}
    answer_latest = {}
    soup = BeautifulSoup(html, 'html.parser')
    for span in soup.find_all('span'):
        span_id = int(span['id'])
        if span_id in answer_text.keys():
            # If a span occurs multiple times, make the answer equal to the region spanning both spans
            before_txt = all_previous_text(span)
            if len(before_txt) < answer_start[span_id]:
                answer_earliest[span_id] = span
            if len(before_txt) + len(span.get_text()) > answer_start[span_id] + len(answer_text[span_id]):
                answer_latest[span_id] = span
            start = len(all_previous_text(answer_earliest[span_id]))
            end = len(all_previous_text(answer_latest[span_id])) + len(answer_latest[span_id].get_text())

            if False and not soup.get_text()[start:end].startswith(answer_earliest[span_id].get_text()) or not soup.get_text()[start:end].endswith(answer_latest[span_id].get_text()):
                print("::")
                print(html)
                print("::")
                print(soup.get_text())
                print("::")
                print(soup.get_text()[start:end])
                print("::")
                print(answer_earliest[span_id].get_text())
                print(all_previous_text(answer_earliest[span_id]))
                print("::")
                print(answer_latest[span_id].get_text())
                print(all_previous_text(answer_latest[span_id]))
            assert soup.get_text()[start:end].startswith(answer_earliest[span_id].get_text())
            assert soup.get_text()[start:end].endswith(answer_latest[span_id].get_text())
            answer_text[span_id] = soup.get_text()[start:end]
            answer_start[span_id] = start
            print("Update:: %s" % answer_text[span_id])
        else:
            answer_earliest[span_id] = span
            answer_latest[span_id] = span
            answer_text[span_id] = span.get_text()
            answer_start[span_id] = len(all_previous_text(span))
    return answer_text, answer_start

def all_previous_text(e):
    #print("HANDLING: " + e.get_text())
    prev = e.previous_sibling
    now = e
    while prev is None:
        prev = now.parent
        if prev is None:
            break
        else:
            now = prev
            prev = prev.previous_sibling
    result = ""
    while prev is not None:
        if hasattr(prev, 'get_text'):
            result = str(prev.get_text()) + result
        else:
            result = str(prev) + result
        #print(":" + result)
        now = prev
        prev = prev.previous_sibling
        while prev is None:
            prev = now.parent
            if prev is None:
                break
            else:
                now = prev
                prev = prev.previous_sibling
    return result

if __name__=="__main__":
    #html = """<div id="1198">Samtidigt importerade <span id="0">centralasiatiska muslimer</span> mongolerna att fungera som administratörer i Kina, mongolerna skickade också <span id="1">hankineser och Khitans</span> från Kina att fungera som administratörer över den muslimska befolkningen i <span id="3">Bukhara</span> i Centralasien, med hjälp av utlänningar att inskränka kraften i den lokala folk från båda länderna. Han kinesiska flyttades till Centralasien områden som <span id="4">Besh Baliq, Almaliq och Samarqand</span> av mongolerna där de arbetade som <span id="4">hantverkare och bönder.</span> Alans rekryterades till de mongolska styrkorna med en enhet som kallas &quot;Right Alan Guard&quot; som kombinerades med &quot;nyligen överlämnade&quot; soldater, mongoler och kinesiska soldater stationerade i området i det förra kungariket Qocho och i Besh Balikh upprättade mongolerna en kines militärkoloni ledd av den kinesiska generalen Qi Kongzhi (Ch&#39;i Kung-chih). Efter den mongoliska erövringen av Centralasien av Genghis Khan valdes utlänningar som administratörer och samförvaltning med kinesiska och Qara-khtier (khitaner) av trädgårdar och fält i Samarqand sattes på muslimerna som ett krav eftersom muslimer inte fick hantera utan dem. Den mongoliska utsedd guvernör Samarqand <span id="5">var Qara-Khitay (Khitan)</span> höll titeln Taishi, bekant med den kinesiska kulturen hans namn var <span id="6">Ahai</span></div>
    #"""
    html = """<div id="137">Innan den egentliga forskningen uttryckligen ägnas åt komplexitet algoritm problem började, <span id="2"><span id="1"><span id="0">var</span> många <span id="0">stiftelser som anges</span></span> av olika forskare.</span> Mest inflytelserika bland dessa var definitionen av <span id="4">Turingmaskiner</span> <span id="3">Alan Turing</span> <span id="5">1936,</span> som visade sig vara en mycket robust och flexibel förenkling av <span id="6">en dator.</span></div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    #print(soup.get_text())
    #print([e.get_text() for e in soup.find_all('span')])
    print("\n".join([all_previous_text(e)+"|"+e.get_text() for e in soup.find_all('span')]))
    #print([int(e['id']) for e in soup.find_all('span')])
    #a,b = get_answers_and_answer_starts(html)
    #print(a.items())
    #print(b.items())