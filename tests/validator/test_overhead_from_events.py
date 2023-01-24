
class TestGetOverheadFromEvents()

        for sat in list_of_satellites.satellites:
            t, events = sat.find_events(coordinates, t0, t1, altitude_degrees=reservation.facility.angle_of_visibility_cone)

            for ti, event in zip(t, events):
                if event == 0:
                    if end == 0:
                        # last interference occurrence has no end (ends with reservation)
                        # save last interference occurrence
                        end = reservation.time.end
                        time_window = TimeWindow(begin=begin, end=end)
                        overhead = OverheadWindow(sat, time_window)
                        overhead_window_list.append(overhead)
                    else:
                        # last interference occurrence has end
                        # do nothing
                        continue
                    begin = ti
                    end = 0 #start tracking new interference occurrence
                elif event == 2:
                    #event 2 in skyfield api is sat leaving overhead. Event we are tracking has end event
                    #so set end to ti of end event and append to interferers
                    end = ti
                    time_window = TimeWindow(begin, end)
                    overhead = OverheadWindow(sat, time_window)
                    overhead_window_list.append(overhead)
        return overhead_window_list