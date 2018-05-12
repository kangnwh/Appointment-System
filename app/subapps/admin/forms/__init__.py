APPT_LI = """
<li class="list-group-item">
        <div class="row">
            <div class="col-md-2">
                {date}
            </div>
            <div class="col-md-2">
                {slot}
            </div>
            <div class="col-md-3">
                {type}

            </div>
            <div class="col-md-2">
                {status}
            </div>

            <div class="col-md-3">
                <div class="btn-group" role="group">
                        <a class="btn btn-warning"
                           href="{url}">
                            Reschedule
                        </a>
                        <a class="btn btn-danger"
                           href="#">Delete</a>
                </div>
            </div>
        </div>
    </li>
"""
def appt_li(date,type,status,url):
    APPT_LI_one = '<li class="list-group-item"><div class="row"><div class="col-md-2">'+ \
                  date +\
                  '</div><div class="col-md-2">{slot}</div><div class="col-md-3">'+ \
                  type +'</div><div class="col-md-2">'+ \
                  status +'</div><div class="col-md-3"><div class="btn-group" role="group"><a class="btn btn-warning" href="'+\
                  url +'"> Reschedule </a><a class="btn btn-danger"  href="#">Delete</a></div></div></div></li>'
