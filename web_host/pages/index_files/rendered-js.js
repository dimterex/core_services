moment.updateLocale('en', {
  week: {
    dow: 1, // Monday is the first day of the week.
  }
});


var today = moment();
window.Calendar = Calendar;

var calendar = null;

class DayStatistic {
  constructor(duration, dayElement) {
    this.update_element(dayElement);
    this.update_duration(duration);
  }

  update_duration(duration) {
    this.duration = duration;

    if (this.dayElement === undefined)
      return;

    this.update_state();
  }

  update_element(element) {
    if (element == null)
      return;

    this.dayElement = element;

    this.update_state();
  }

  update_state() {
    if (this.duration > 7) {
      if (!this.dayElement.classList.contains("day-writed")) {
        this.dayElement.classList.add("day-writed");
      }
    }
    else {
      this.dayElement.classList.remove("day-writed");
    }
  }
}


function Calendar(selector) {
  this.el = document.getElementById(selector);
  this.events = [];
  this.statistics = {};
  this.history = {};
  this.current = moment().date(1);
  this.draw();
  var current = document.querySelector('.today');
  if(current) {
    var self = this;
    window.setTimeout(function() {
      self.openDay(current);
    }, 500);
  }
}

Calendar.prototype.update_requests = function(month, year) {
  var requested = this.history[year];
  month += 1;
  if (requested === undefined){
    this.history[year] = [];
    this.history[year].push(month);
    getMonthStatistics(this, month, year);
  } else {
    if (!requested.includes(month)) {
      requested.push(month);
      getMonthStatistics(this, month, year);
    }
  }
}

Calendar.prototype.update_statistics = function(data) {
  var self = this;
  data.forEach(element => {
    var dayElement = self.statistics[element.date];
    if (dayElement) {
      dayElement.update_duration(element.duration);
    } else {
      self.statistics[element.date] = new DayStatistic(element.duration, null);
    }
  });
}

Calendar.prototype.draw = function() {
  //Create Header
  this.drawHeader();

  //Draw Month
  this.drawMonth();

  this.drawLegend();
}

Calendar.prototype.drawHeader = function() {
  var self = this;
  if(!this.header) {
    //Create the header elements
    this.header = createElement('div', 'header');
    this.header.className = 'header';

    this.title = createElement('h1');

    var right = createElement('div', 'right');
    right.addEventListener('click', function() { self.nextMonth(); });

    var left = createElement('div', 'left');
    left.addEventListener('click', function() { self.prevMonth(); });

    //Append the Elements
    this.header.appendChild(this.title); 
    this.header.appendChild(right);
    this.header.appendChild(left);
    this.el.appendChild(this.header);
  }

  this.title.innerHTML = this.current.format('MMMM YYYY');
}

Calendar.prototype.drawMonth = function() {
  var self = this;
  if(this.month) {
    this.oldMonth = this.month;
    this.oldMonth.className = 'month out ' + (self.next ? 'next' : 'prev');
    this.oldMonth.addEventListener('webkitAnimationEnd', function() {
      self.oldMonth.parentNode.removeChild(self.oldMonth);
      self.month = createElement('div', 'month');
      self.backFill();
      self.currentMonth();
      self.fowardFill();
      self.el.appendChild(self.month);
      window.setTimeout(function() {
        self.month.className = 'month in ' + (self.next ? 'next' : 'prev');
      }, 16);
    });
  } else {
      this.month = createElement('div', 'month');
      this.el.appendChild(this.month);
      this.backFill();
      this.currentMonth();
      this.fowardFill();
      this.month.className = 'month new';
  }
}

Calendar.prototype.backFill = function() {
  var clone = this.current.clone();
  var dayOfWeek = clone.day();

  if(!dayOfWeek) { return; }

  clone.subtract('days', dayOfWeek+1);

  for(var i = dayOfWeek; i > 0 ; i--) {
    this.drawDay(clone.add('days', 1));
  }
}

Calendar.prototype.fowardFill = function() {
  var clone = this.current.clone().add('months', 1).subtract('days', 1);
  var dayOfWeek = clone.day();

  if(dayOfWeek === 6) { return; }

  for(var i = dayOfWeek; i < 6 ; i++) {
    this.drawDay(clone.add('days', 1));
  }
}

Calendar.prototype.currentMonth = function() {
  var clone = this.current.clone();

  while(clone.month() === this.current.month()) {
    this.drawDay(clone);
    clone.add('days', 1);
  }
}

Calendar.prototype.getWeek = function(day) {
  if(!this.week || day.day() === 0) {
    this.week = createElement('div', 'week');
    this.month.appendChild(this.week);
  }
}

Calendar.prototype.drawDay = function(day) {
  var self = this;
  this.getWeek(day);
  //console.log(day);

  //Outer Day
  var outer = createElement('div', this.getDayClass(day));
  outer.addEventListener('click', function() {
    self.openDay(this);
  });

  //Day Name
  var name = createElement('div', 'day-name', day.format('ddd'));

  //Day Number
  var number = createElement('div', 'day-number', day.format('DD'));
  var dayFormat = day.format('YYYY-MM-DD');
  var element = this.statistics[dayFormat];
  if (element === undefined) {
     this.statistics[dayFormat] = new DayStatistic(0, number);
  } else {
    element.update_element(number);
  }

  //Events
  var events = createElement('div', 'day-events');
  this.drawEvents(day, events);

  outer.appendChild(name);
  outer.appendChild(number);
  outer.appendChild(events);
  this.week.appendChild(outer);
}

Calendar.prototype.drawEvents = function(day, element) {
  if(day.month() === this.current.month()) {
    var todaysEvents = this.events.reduce(function(memo, ev) {
      if(ev.date.isSame(day, 'day')) {
        memo.push(ev);
      }
      return memo;
    }, []);

    todaysEvents.forEach(function(ev) {
      var evSpan = createElement('span', ev.color);
      element.appendChild(evSpan);
    });
  }
}

Calendar.prototype.getDayClass = function(day) {
  classes = ['day'];
  if(day.month() !== this.current.month()) {
    classes.push('other');
  } else if (today.isSame(day, 'day')) {
    classes.push('today');
  }
  return classes.join(' ');
}

Calendar.prototype.openDay = function(el) {

  var details, arrow;
  var dayNumber = +el.querySelectorAll('.day-number')[0].innerText || +el.querySelectorAll('.day-number')[0].textContent;
  var day = this.current.clone().date(dayNumber);

  var currentOpened = document.querySelector('.details');

  //Check to see if there is an open detais box on the current row
  if(currentOpened && currentOpened.parentNode === el.parentNode) {
    details = currentOpened;
    arrow = document.querySelector('.arrow');
  } else {
    //Close the open events on differnt week row
    //currentOpened && currentOpened.parentNode.removeChild(currentOpened);
    if(currentOpened) {
      currentOpened.addEventListener('webkitAnimationEnd', function() {
        currentOpened.parentNode.removeChild(currentOpened);
      });
      currentOpened.addEventListener('oanimationend', function() {
        currentOpened.parentNode.removeChild(currentOpened);
      });
      currentOpened.addEventListener('msAnimationEnd', function() {
        currentOpened.parentNode.removeChild(currentOpened);
      });
      currentOpened.addEventListener('animationend', function() {
        currentOpened.parentNode.removeChild(currentOpened);
      });
      currentOpened.className = 'details out';
    }

    //Create the Details Container
    details = createElement('div', 'details in');

    //Create the arrow
    var arrow = createElement('div', 'arrow');

    //Create the event wrapper

    details.appendChild(arrow);
    el.parentNode.appendChild(details);
  }

  var todaysEvents = this.events.reduce(function(memo, ev) {
    if(ev.date.isSame(day, 'day')) {
      memo.push(ev);
    }
    return memo;
  }, []);

  this.renderEvents(todaysEvents, details);

  arrow.style.left = el.offsetLeft - el.parentNode.offsetLeft + 27 + 'px';
}

Calendar.prototype.renderEvents = function(events, ele) {
  //Remove any events in the current details element
  var currentWrapper = ele.querySelector('.events');
  var wrapper = createElement('div', 'events in' + (currentWrapper ? ' new' : ''));

  events.forEach(function(ev) {
    var div = createElement('div', 'event');
    var square = createElement('div', 'event-category ' + ev.color);
    var span = createElement('span', '', ev.eventName);

    div.appendChild(square);
    div.appendChild(span);
    wrapper.appendChild(div);
  });

  if(!events.length) {
    var div = createElement('div', 'event empty');
    var span = createElement('span', '', 'No Events');

    div.appendChild(span);
    wrapper.appendChild(div);
  }

  if(currentWrapper) {
    currentWrapper.className = 'events out';
    currentWrapper.addEventListener('webkitAnimationEnd', function() {
      currentWrapper.parentNode.removeChild(currentWrapper);
      ele.appendChild(wrapper);
    });
    currentWrapper.addEventListener('oanimationend', function() {
      currentWrapper.parentNode.removeChild(currentWrapper);
      ele.appendChild(wrapper);
    });
    currentWrapper.addEventListener('msAnimationEnd', function() {
      currentWrapper.parentNode.removeChild(currentWrapper);
      ele.appendChild(wrapper);
    });
    currentWrapper.addEventListener('animationend', function() {
      currentWrapper.parentNode.removeChild(currentWrapper);
      ele.appendChild(wrapper);
    });
  } else {
    ele.appendChild(wrapper);
  }
}

Calendar.prototype.drawLegend = function() {
  var legend = createElement('div', 'legend');
  var calendars = this.events.map(function(e) {
    return e.calendar + '|' + e.color;
  }).reduce(function(memo, e) {
    if(memo.indexOf(e) === -1) {
      memo.push(e);
    }
    return memo;
  }, []).forEach(function(e) {
    var parts = e.split('|');
    var entry = createElement('span', 'entry ' +  parts[1], parts[0]);
    legend.appendChild(entry);
  });
  this.el.appendChild(legend);
}

Calendar.prototype.nextMonth = function() {
  this.current.add('months', 1);
  this.update_requests(this.current.month(), this.current.year());
  this.next = true;
  this.draw();
}

Calendar.prototype.prevMonth = function() {
  this.current.subtract('months', 1);
  this.update_requests(this.current.month(), this.current.year());
  this.next = false;
  this.draw();
}

function createElement(tagName, className, innerText) {
  var ele = document.createElement(tagName);
  if(className) {
    ele.className = className;
  }
  if(innerText) {
    ele.innderText = ele.textContent = innerText;
  }
  return ele;
}


function on_load() {
    calendar = new Calendar('calendar');
    var ws = new WebSocketService(60009);
    ws.configure('get_worklogs_response', function(data) {
      calendar.update_statistics(data.worklogs);
    })
    ws.configure('get_events_response', function(data) {
      console.log(data)
    })

    getMonthStatistics(calendar, today.month()+1, today.year())

    //ws.send(`{ "type": "get_worklogs_request", "value": { "promise_id": 1, "year": ${today.year()}, "month": ${today.month()+1} } }`);
    // ws.send(`{ "type": "get_events_request", "value": { "promise_id": 2, "date": "${today.format('Y-M-D h:mm:ss')}" } }`);
    // ws.send(`{ "type": "get_events_request", "value": { "promise_id": 2, "date": "2022-11-30 00:00:00" } }`);
}
