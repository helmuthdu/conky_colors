--[[
-- This code is mostly by londonali1010, mrpeachy, VinDSL, Wlourf and SLK
-- Conky-Colors by helmuthdu
-- license : Distributed under the terms of GNU GPL version 2 or later
]]

require 'cairo'

-------------------------------------------------------------------------------
--                                                                 rgb_to_r_g_b
-- converts color in hexa to decimal
--
function rgb_to_r_g_b(colour, alpha)
	return ((colour / 0x10000) % 0x100) / 255., ((colour / 0x100) % 0x100) / 255., (colour % 0x100) / 255., alpha
end

-------------------------------------------------------------------------------
--                                                                 get_user_dir
-- return user dir
--
function get_user_dir()
	local f = assert(io.popen("conky-colors --localdir"))
	local s = assert(f:read('*l'))
	f:close()
	return s
end

-------------------------------------------------------------------------------
--                                                             get_weather_info
-- return yahoo weather info
--
function get_yahoo_weather_info(dataType, dataLocation, dataUnit)
	local f = assert(io.popen("conky-colors --systemdir"))
	local s = assert(f:read('*l'))
	f:close()
	f = assert(io.popen("sh " .. s .. "/bin/conkyYahooWeather " .. dataType .. " " .. dataLocation .. " " .. dataUnit)) -- runs command
	s = assert(f:read('*l'))
	f:close()
	return s
end

-------------------------------------------------------------------------------
--                                                                 get_day_name
-- return day name
--
function get_day_name(format, day)
	local f = assert(io.popen("date " .. format .. " --date=" .. day)) -- runs command
	local s = assert(f:read('*l'))
	f:close()
	return s
end
-------------------------------------------------------------------------------
--                                                            get_music_percent
-- return music percent
--
function get_music_percent (player)
	local f = assert(io.popen("conky-colors --systemdir"))
	local s = assert(f:read('*l'))
	f:close()
	f = assert(io.popen("sh " .. s .. "/bin/conky" .. player .. " --datatype=PP")) -- runs command
	s = assert(f:read('*a'))
	f:close()
	return s
end

-------------------------------------------------------------------------------
--                                                                      weather
-- dispay text
--
function display_text(data)

	local txt = data.txt
	local x, y = data.x, data.y
	local txt_weight, txt_size = data.txt_weight, data.txt_size
	local txt_fg_colour, txt_fg_alpha = data.txt_fg_colour, data.txt_fg_alpha
	if data.font==nil then data.font = "ubuntu" end
	cairo_select_font_face (cr, data.font, CAIRO_FONT_SLANT_NORMAL, txt_weight)
	cairo_set_font_size (cr, txt_size)
	cairo_set_source_rgba (cr, rgb_to_r_g_b(txt_fg_colour, txt_fg_alpha))
	cairo_move_to (cr, x - (txt_size / 2), y)
	cairo_show_text (cr, txt)
	cairo_stroke (cr)
end

-------------------------------------------------------------------------------
--                                                                  clock_hands
-- display clock hands
--
function clock_hands(data)

	local xc = data.xc
	local yc = data.yc
	local colour = data.colour
	local alpha = data.alpha
	local show_secs = data.show_secs
	local size = data.size
	local secs,mins,hours,secs_arc,mins_arc,hours_arc
	local xh,yh,xm,ym,xs,ys

	secs=os.date("%S")
	mins=os.date("%M")
	hours=os.date("%I")

	secs_arc=(2*math.pi/60)*secs
	mins_arc=(2*math.pi/60)*mins+secs_arc/60
	hours_arc=(2*math.pi/12)*hours+mins_arc/12

	xh=xc+0.4*size*math.sin(hours_arc)
	yh=yc-0.4*size*math.cos(hours_arc)
	cairo_move_to(cr,xc,yc)
	cairo_line_to(cr,xh,yh)

	cairo_set_line_cap(cr,CAIRO_LINE_CAP_ROUND)
	cairo_set_line_width(cr,5)
	cairo_set_source_rgba(cr,rgb_to_r_g_b(colour,alpha))
	cairo_stroke(cr)

	xm=xc+0.5*size*math.sin(mins_arc)
	ym=yc-0.5*size*math.cos(mins_arc)
	cairo_move_to(cr,xc,yc)
	cairo_line_to(cr,xm,ym)

	cairo_set_line_width(cr,3)
	cairo_stroke(cr)

	if show_secs then
		xs=xc+0.5*size*math.sin(secs_arc)
		ys=yc-0.5*size*math.cos(secs_arc)
		cairo_move_to(cr,xc,yc)
		cairo_line_to(cr,xs,ys)

		cairo_set_line_width(cr,1)
		cairo_stroke(cr)
	end

	cairo_set_line_cap(cr,CAIRO_LINE_CAP_BUTT)
end

-------------------------------------------------------------------------------
--                                                              draw_clock_ring
-- displays clock
--
function draw_clock_ring(data)
	local value = data.value
	local value_max = data.value_max
	local x, y = data.x, data.y
	local graph_radius = data.graph_radius
	local graph_thickness, graph_unit_thickness = data.graph_thickness, data.graph_unit_thickness
	local graph_unit_angle = data.graph_unit_angle
	local graph_bg_colour, graph_bg_alpha = data.graph_bg_colour, data.graph_bg_alpha
	local graph_fg_colour, graph_fg_alpha = data.graph_fg_colour, data.graph_fg_alpha

	-- background ring
	cairo_arc(cr, x, y, graph_radius, 0, 2 * math.pi)
	cairo_set_source_rgba(cr, rgb_to_r_g_b(graph_bg_colour, graph_bg_alpha))
	cairo_set_line_width(cr, graph_thickness)
	cairo_stroke(cr)

	-- arc of value
	local val = (value % value_max)
	local i = 1
	while i <= val do
		cairo_arc(cr, x, y, graph_radius,(  ((graph_unit_angle * i) - graph_unit_thickness)*(2*math.pi/360)  )-(math.pi/2),((graph_unit_angle * i) * (2*math.pi/360))-(math.pi/2))
		cairo_set_source_rgba(cr,rgb_to_r_g_b(graph_fg_colour,graph_fg_alpha))
		cairo_stroke(cr)
		i = i + 1
	end
	local angle = (graph_unit_angle * i) - graph_unit_thickness

	-- graduations marks
	local graduation_radius = data.graduation_radius
	local graduation_thickness, graduation_mark_thickness = data.graduation_thickness, data.graduation_mark_thickness
	local graduation_unit_angle = data.graduation_unit_angle
	local graduation_fg_colour, graduation_fg_alpha = data.graduation_fg_colour, data.graduation_fg_alpha
	if graduation_radius > 0 and graduation_thickness > 0 and graduation_unit_angle > 0 then
		local nb_graduation = 360 / graduation_unit_angle
		local i = 1
		while i <= nb_graduation do
			cairo_set_line_width(cr, graduation_thickness)
			cairo_arc(cr, x, y, graduation_radius, (((graduation_unit_angle * i)-(graduation_mark_thickness/2))*(2*math.pi/360))-(math.pi/2),(((graduation_unit_angle * i)+(graduation_mark_thickness/2))*(2*math.pi/360))-(math.pi/2))
			cairo_set_source_rgba(cr,rgb_to_r_g_b(graduation_fg_colour,graduation_fg_alpha))
			cairo_stroke(cr)
			cairo_set_line_width(cr, graph_thickness)
			i = i + 1
		end
	end

	-- text
	local txt_radius = data.txt_radius
	local txt_weight, txt_size = data.txt_weight, data.txt_size
	local txt_fg_colour, txt_fg_alpha = data.txt_fg_colour, data.txt_fg_alpha
	local movex = txt_radius * (math.cos((angle * 2 * math.pi / 360)-(math.pi/2)))
	local movey = txt_radius * (math.sin((angle * 2 * math.pi / 360)-(math.pi/2)))
	cairo_select_font_face (cr, "ubuntu", CAIRO_FONT_SLANT_NORMAL, txt_weight);
	cairo_set_font_size (cr, txt_size);
	cairo_set_source_rgba (cr, rgb_to_r_g_b(txt_fg_colour, txt_fg_alpha));
	cairo_move_to (cr, x + movex - (txt_size / 2), y + movey + 3);
	cairo_show_text (cr, value);
	cairo_stroke (cr);
end

-------------------------------------------------------------------------------
--                                                            angle_to_position
-- convert degree to rad and rotate (0 degree is top/north)
--
function angle_to_position(start_angle, current_angle)
	local pos = current_angle + start_angle
	return ( ( pos * (2 * math.pi / 360) ) - (math.pi / 2) )
end

-------------------------------------------------------------------------------
--                                                              draw_gauge_ring
-- display gauges
--
function draw_gauge_ring(data)
	local value = data.value
	local value_max = data.value_max
	local x, y = data.x, data.y
	local graph_radius = data.graph_radius
	local graph_thickness, graph_unit_thickness = data.graph_thickness, data.graph_unit_thickness
	local graph_start_angle = data.graph_start_angle
	local graph_unit_angle = data.graph_unit_angle
	local graph_bg_colour, graph_bg_alpha = data.graph_bg_colour, data.graph_bg_alpha
	local graph_fg_colour, graph_fg_alpha = data.graph_fg_colour, data.graph_fg_alpha
	local hand_fg_colour, hand_fg_alpha = data.hand_fg_colour, data.hand_fg_alpha
	local graph_end_angle = (value_max * graph_unit_angle) % 360

	if value == nil then value=0  end

	-- background ring
	cairo_arc(cr, x, y, graph_radius, angle_to_position(graph_start_angle, 0), angle_to_position(graph_start_angle, graph_end_angle))
	cairo_set_source_rgba(cr, rgb_to_r_g_b(graph_bg_colour, graph_bg_alpha))
	cairo_set_line_width(cr, graph_thickness)
	cairo_stroke(cr)

	-- arc of value
	local val = value % (value_max + 1)
	local start_arc = 0
	local stop_arc = 0
	local i = 1
	while i <= val do
		start_arc = (graph_unit_angle * i) - graph_unit_thickness
		stop_arc = (graph_unit_angle * i)
		cairo_arc(cr, x, y, graph_radius, angle_to_position(graph_start_angle, start_arc), angle_to_position(graph_start_angle, stop_arc))
		cairo_set_source_rgba(cr, rgb_to_r_g_b(graph_fg_colour, graph_fg_alpha))
		cairo_stroke(cr)
		i = i + 1
	end
	local angle = start_arc

	-- hand
	start_arc = (graph_unit_angle * val) - (graph_unit_thickness * 2)
	stop_arc = (graph_unit_angle * val)
	cairo_arc(cr, x, y, graph_radius, angle_to_position(graph_start_angle, start_arc), angle_to_position(graph_start_angle, stop_arc))
	cairo_set_source_rgba(cr, rgb_to_r_g_b(hand_fg_colour, hand_fg_alpha))
	cairo_stroke(cr)

	-- graduations marks
	local graduation_radius = data.graduation_radius
	local graduation_thickness, graduation_mark_thickness = data.graduation_thickness, data.graduation_mark_thickness
	local graduation_unit_angle = data.graduation_unit_angle
	local graduation_fg_colour, graduation_fg_alpha = data.graduation_fg_colour, data.graduation_fg_alpha
	if graduation_radius > 0 and graduation_thickness > 0 and graduation_unit_angle > 0 then
		local nb_graduation = graph_end_angle / graduation_unit_angle
		local i = 0
		while i < nb_graduation do
			cairo_set_line_width(cr, graduation_thickness)
			start_arc = (graduation_unit_angle * i) - (graduation_mark_thickness / 2)
			stop_arc = (graduation_unit_angle * i) + (graduation_mark_thickness / 2)
			cairo_arc(cr, x, y, graduation_radius, angle_to_position(graph_start_angle, start_arc), angle_to_position(graph_start_angle, stop_arc))
			cairo_set_source_rgba(cr,rgb_to_r_g_b(graduation_fg_colour,graduation_fg_alpha))
			cairo_stroke(cr)
			cairo_set_line_width(cr, graph_thickness)
			i = i + 1
		end
	end

	-- text
	local txt_radius = data.txt_radius
	local txt_weight, txt_size = data.txt_weight, data.txt_size
	local txt_fg_colour, txt_fg_alpha = data.txt_fg_colour, data.txt_fg_alpha
	local movex = txt_radius * math.cos(angle_to_position(graph_start_angle, angle))
	local movey = txt_radius * math.sin(angle_to_position(graph_start_angle, angle))
	cairo_select_font_face (cr, "ubuntu", CAIRO_FONT_SLANT_NORMAL, txt_weight)
	cairo_set_font_size (cr, txt_size)
	cairo_set_source_rgba (cr, rgb_to_r_g_b(txt_fg_colour, txt_fg_alpha))
	cairo_move_to (cr, x + movex - (txt_size / 2), y + movey + 3)
	cairo_show_text (cr, value)
	cairo_stroke (cr)

	-- caption
	local caption = data.caption
	local caption_weight, caption_size = data.caption_weight, data.caption_size
	local caption_fg_colour, caption_fg_alpha = data.caption_fg_colour, data.caption_fg_alpha
	local tox = graph_radius * (math.cos((graph_start_angle * 2 * math.pi / 360)-(math.pi/2)))
	local toy = graph_radius * (math.sin((graph_start_angle * 2 * math.pi / 360)-(math.pi/2)))
	cairo_select_font_face (cr, "ubuntu", CAIRO_FONT_SLANT_NORMAL, caption_weight);
	cairo_set_font_size (cr, caption_size)
	cairo_set_source_rgba (cr, rgb_to_r_g_b(caption_fg_colour, caption_fg_alpha))
	cairo_move_to (cr, x + tox + 5, y + toy + 3)
	-- bad hack but not enough time !
	if graph_start_angle < 105 then
		cairo_move_to (cr, x + tox - 30, y + toy + 1)
	end
	cairo_show_text (cr, caption)
	cairo_stroke (cr)
end

-------------------------------------------------------------------------------
--                                                                    draw_ring
-- simple rings
--
function draw_ring(data)

	local value = data.value
	local value_max = data.value_max
	local bgc = data.bg_colour
	local bga = data.bg_alpha
	local fgc = data.fg_colour
	local fga = data.fg_alpha
	local xc, yc = data.x, data.y
	local radius = data.radius
	local thickness = data.thickness
	local sa = data.start_angle
	local ea = data.end_angle
	local lr = data.lr
	if value == nil then value=0  end
	local pct = value/value_max

	local angle_0 = sa * math.pi/180 - math.pi/2
	local angle_f = ea * math.pi/180 - math.pi/2
	local pct_arc = pct * (angle_f - angle_0)

	-- Draw background ring
	cairo_arc(cr, xc, yc, radius, angle_0, angle_f)
	cairo_set_source_rgba(cr, rgb_to_r_g_b(bgc, bga))
	cairo_set_line_width(cr, thickness)
	cairo_stroke(cr)

	-- Draw indicator ring
	cairo_arc(cr, xc, yc, radius, angle_0, angle_0 + pct_arc)
	cairo_set_source_rgba(cr, rgb_to_r_g_b(fgc, fga))
	cairo_stroke(cr)
end

-------------------------------------------------------------------------------
--                                                              draw_gauge_bars
-- display gauge
--
function draw_gauge_bars(data)
	local x=data.x
	local y=data.y
	local divisions=data.divisions
	local div_width=data.div_width
	local div_height=data.div_height
	local div_gap=data.div_gap
	local br,bg,bb,ba=rgb_to_r_g_b(data.bg_color, data.bg_alpha)
	local sr,sg,sb,sa=rgb_to_r_g_b(data.st_color, data.fg_alpha)
	local mr,mg,mb,ma=rgb_to_r_g_b(data.mid_color, data.fg_alpha)
	local er,eg,eb,ea=rgb_to_r_g_b(data.end_color, data.fg_alpha)

	if data.value==nil then value=0 else value=data.value end

	local value_max=data.value_max
	local value_divs=(value/value_max)*divisions

	cairo_set_line_width (cr,div_width)

	for i=1,divisions do
		if i<(divisions/2) and i<=value_divs then
			colr=((mr-sr)*(i/(divisions/2)))+sr
			colg=((mg-sg)*(i/(divisions/2)))+sg
			colb=((mb-sb)*(i/(divisions/2)))+sb
			cola=((ma-sa)*(i/(divisions/2)))+sa
		elseif i>=(divisions/2) and i<=value_divs then
			colr=((er-mr)*((i-(divisions/2))/(divisions/2)))+mr
			colg=((eg-mg)*((i-(divisions/2))/(divisions/2)))+mg
			colb=((eb-mb)*((i-(divisions/2))/(divisions/2)))+mb
			cola=((ea-ma)*((i-(divisions/2))/(divisions/2)))+ma
		else
			colr=br
			colg=bg
			colb=bb
			cola=ba
		end

		cairo_set_source_rgba (cr,colr,colg,colb,cola)
		if data.orientation == "horizontal" then
			cairo_move_to (cr,x+((div_width+div_gap)*i-1),y)
		else
			cairo_move_to (cr,x,y-((div_width+div_gap)*i-1))
		end
		cairo_rel_line_to (cr,0,div_height)
		cairo_stroke (cr)
	end
end--function bars


-------------------------------------------------------------------------------
--                                                                     draw_box
-- display background
--

--[[BOX WIDGET v1.1 by Wlourf 27/01/2011
This widget can drawn some boxes, even circles in your conky window
http://u-scripts.blogspot.com/2011/01/box-widget.html)

Inspired by Background by londonali1010 (2009), thanks ;-)

The parameters (all optionals) are :
x           - x coordinate of top-left corner of the box, default = 0 = (top-left corner of conky window)
y           - y coordinate of top-left corner of the box, default = 0 = (top-left corner of conky window)
w           - width of the box, default = width of the conky window
h           - height of the box, default = height of the conky window
corners     - corners is a table for the four corners in this order : top-left, top-right,bottom-right, bottom-left
              each corner is defined in a table with a shape and a radius, available shapes are : "curve","circle","line"
              example for the same shapes for all corners:
              { {"circle",10} }
              example for first corner different from the three others
              { {"circle",10}, {"circle",5}  }
              example for top corners differents from bottom corners
              { {"circle",10}, {"circle",10}, {"line",0}  }
              default = { {"line",0} } i.e=no corner
operator    - set the compositing operator (needs in the conkyrc : own_window_argb_visual yes)
              see http://cairographics.org/operators/
              available operators are :
              "clear","source","over","in","out","atop","dest","dest_over","dest_in","dest_out","dest_atop","xor","add","saturate"
              default = "over"
border      - if border>0, the script draws only the border, like a frame, default=0
dash        - if border>0 and dash>0, the border is draw with dashes, default=0
skew_x      - skew box around x axis, default = 0
skew_y      - skew box around y axis, default = 0
scale_x     - rescale the x axis, default=1, useful for drawing elipses ...
scale_y     - rescale the x axis, default=1
angle	    - angle of rotation of the box in degrees, default = 0
              i.e. a horizontal graph
rot_x       - x point of rotation's axis, default = 0,
              relative to top-left corner of the box, (not the conky window)
rot_y       - y point of rotation's axis, default = 0
              relative to top-left corner of the box, (not the conky window)
draw_me     - if set to false, box is not drawn (default = true or 1)
              it can be used with a conky string, if the string returns 1, the box is drawn :
              example : "${if_empty ${wireless_essid wlan0}}${else}1$endif",

linear_gradient - table with the coordinates of two points to define a linear gradient,
                  points are relative to top-left corner of the box, (not the conky window)
                  {x1,y1,x2,y2}
radial_gradient - table with the coordinates of two circle to define a radial gradient,
                  points are relative to top-left corner of the box, (not the conky window)
                  {x1,y1,r1,x2,y2,r2} (r=radius)
colour      - table of colours, default = plain white {{1,0xFFFFFF,0.5}}
              this table contains one or more tables with format {P,C,A}
              P=position of gradient (0 = start of the gradient, 1= end of the gradient)
              C=hexadecimal colour
              A=alpha (opacity) of color (0=invisible,1=opacity 100%)
              Examples :
              for a plain color {{1,0x00FF00,0.5}}
              for a gradient with two colours {{0,0x00FF00,0.5},{1,0x000033,1}}        {x=80,y=150,w=20,h=20,
        radial_gradient={20,20,0,20,20,20},
        colour={{0.5,0xFFFFFF,1},{1,0x000000,0}},
              or {{0.5,0x00FF00,1},{1,0x000033,1}} -with this one, gradient will start in the middle
              for a gradient with three colours {{0,0x00FF00,0.5},{0.5,0x000033,1},{1,0x440033,1}}
              and so on ...



To call this script in Conky, use (assuming you have saved this script to ~/scripts/):
    lua_load ~/scripts/box.lua
    lua_draw_hook_pre main_box

And leave one line blank or not after TEXT
]]

function draw_box(data)

	if data.draw_me == true then data.draw_me = nil end
	if data.draw_me ~= nil and conky_parse(tostring(data.draw_me)) ~= "1" then return end

	local table_corners={"circle","curve","line"}

	local t_operators={
		clear     = CAIRO_OPERATOR_CLEAR,
		source    = CAIRO_OPERATOR_SOURCE,
		over      = CAIRO_OPERATOR_OVER,
		["in"]    = CAIRO_OPERATOR_IN,
		out       = CAIRO_OPERATOR_OUT,
		atop      = CAIRO_OPERATOR_ATOP,
		dest      = CAIRO_OPERATOR_DEST,
		dest_over = CAIRO_OPERATOR_DEST_OVER,
		dest_in   = CAIRO_OPERATOR_DEST_IN,
		dest_out  = CAIRO_OPERATOR_DEST_OUT,
		dest_atop = CAIRO_OPERATOR_DEST_ATOP,
		xor       = CAIRO_OPERATOR_XOR,
		add       = CAIRO_OPERATOR_ADD,
		saturate  = CAIRO_OPERATOR_SATURATE,
	}

	function rgba_to_r_g_b_a(tc)
		--tc={position,colour,alpha}
		local colour = tc[2]
		local alpha = tc[3]
		return ((colour / 0x10000) % 0x100) / 255., ((colour / 0x100) % 0x100) / 255., (colour % 0x100) / 255., alpha
	end

	function table.copy(data)
		local t2 = {}
		for k,v in pairs(data) do
			t2[k] = {v[1],v[2]}
		end
		return t2
	end

	function draw_corner(num,t)
		local shape=t[1]
		local radius=t[2]
		local x,y = t[3],t[4]
		if shape=="line" then
			if num == 1 then cairo_line_to(cr,radius,0)
			elseif num == 2 then cairo_line_to(cr,x,radius)
			elseif num == 3 then cairo_line_to(cr,x-radius,y)
			elseif num == 4 then cairo_line_to(cr,0,y-radius)
			end
		end
		if shape=="circle" then
			local PI = math.pi
			if num == 1 then cairo_arc(cr,radius,radius,radius,-PI,-PI/2)
			elseif num == 2 then cairo_arc(cr,x-radius,y+radius,radius,-PI/2,0)
			elseif num == 3 then cairo_arc(cr,x-radius,y-radius,radius,0,PI/2)
			elseif num == 4 then cairo_arc(cr,radius,y-radius,radius,PI/2,-PI)
			end
		end
		if shape=="curve" then
			if num == 1 then cairo_curve_to(cr,0,radius ,0,0 ,radius,0)
			elseif num == 2 then cairo_curve_to(cr,x-radius,0, x,y, x,radius)
			elseif num == 3 then cairo_curve_to(cr,x,y-radius, x,y, x-radius,y)
			elseif num == 4 then cairo_curve_to(cr,radius,y, x,y, 0,y-radius)
			end
		end
	end

	--check values and set default values
	if data.x == nil then data.x = 0 end
	if data.y == nil then data.y = 0 end
	if data.w == nil then data.w = conky_window.width end
	if data.h == nil then data.h = conky_window.height end
	if data.radius == nil then data.radius = 0 end
	if data.border == nil then data.border = 0 end
	if data.colour==nil then data.colour={{1,0x000000,0.5}} end
	if data.linear_gradient ~= nil then
		if #data.linear_gradient ~= 4 then
			data.linear_gradient = {data.x,data.y,data.width,data.height}
		end
	end
	if data.angle==nil then data.angle = 0 end

	if data.skew_x == nil then data.skew_x=0  end
	if data.skew_y == nil then  data.skew_y=0 end
	if data.scale_x==nil then data.scale_x=1 end
	if data.scale_y==nil then data.scale_y=1 end
	if data.rot_x == nil then data.rot_x=0  end
	if data.rot_y == nil then  data.rot_y=0 end

	if data.operator == nil then data.operator = "over" end
	if (t_operators[data.operator]) == nil then
		print ("wrong operator :",data.operator)
		data.operator = "over"
	end

	if data.radial_gradient ~= nil then
		if #data.radial_gradient ~= 6 then
			data.radial_gradient = {data.x,data.y,0, data.x,data.y, data.width}
		end
	end

	for i=1, #data.colour do
		if #data.colour[i]~=3 then
			print ("error in color table")
			data.colour[i]={1,0xFFFFFF,1}
		end
	end

	if data.corners == nil then data.corners={ {"line",0} } end
	local data_corners = {}
	local data_corners = table.copy(data.corners)
	--don't use data_corners=data.corners otherwise data.corners is altered

	--complete the data_corners table if needed
	for i=#data_corners+1,4 do
		data_corners[i]=data_corners[#data_corners]
		local flag=false
		for j,v in pairs(table_corners) do flag=flag or (data_corners[i][1]==v) end
		if not flag then print ("error in corners table :",data_corners[i][1]);data_corners[i][1]="curve"  end
	end

	--this way :
	--    data_corners[1][4]=x
	--    data_corners[2][3]=y
	--doesn't work
	data_corners[1]={data_corners[1][1],data_corners[1][2],0,0}
	data_corners[2]={data_corners[2][1],data_corners[2][2],data.w,0}
	data_corners[3]={data_corners[3][1],data_corners[3][2],data.w,data.h}
	data_corners[4]={data_corners[4][1],data_corners[4][2],0,data.h}

	data.no_gradient = (data.linear_gradient == nil ) and (data.radial_gradient == nil )

	cairo_save(cr)
	cairo_translate(cr, data.x, data.y)
	if data.rot_x~=0 or data.rot_y~=0 or data.angle~=0 then
		cairo_translate(cr,data.rot_x,data.rot_y)
		cairo_rotate(cr,data.angle*math.pi/180)
		cairo_translate(cr,-data.rot_x,-data.rot_y)
	end
	if data.scale_x~=1 or data.scale_y~=1 or data.skew_x~=0 or data.skew_y~=0 then
		local matrix0 = cairo_matrix_t:create()
		tolua.takeownership(matrix0)
		cairo_matrix_init (matrix0, data.scale_x,math.pi*data.skew_y/180	, math.pi*data.skew_x/180	,data.scale_y,0,0)
		cairo_transform(cr,matrix0)
	end

	local tc=data_corners
	cairo_move_to(cr,tc[1][2],0)
	cairo_line_to(cr,data.w-tc[2][2],0)
	draw_corner(2,tc[2])
	cairo_line_to(cr,data.w,data.h-tc[3][2])
	draw_corner(3,tc[3])
	cairo_line_to(cr,tc[4][2],data.h)
	draw_corner(4,tc[4])
	cairo_line_to(cr,0,tc[1][2])
	draw_corner(1,tc[1])

	if data.no_gradient then
		cairo_set_source_rgba(cr,rgba_to_r_g_b_a(data.colour[1]))
	else
		if data.linear_gradient ~= nil then
			pat = cairo_pattern_create_linear (data.linear_gradient[1],data.linear_gradient[2],data.linear_gradient[3],data.linear_gradient[4])
		elseif data.radial_gradient ~= nil then
			pat = cairo_pattern_create_radial (data.radial_gradient[1],data.radial_gradient[2],data.radial_gradient[3],
			data.radial_gradient[4],data.radial_gradient[5],data.radial_gradient[6])
		end
		for i=1, #data.colour do
			cairo_pattern_add_color_stop_rgba (pat, data.colour[i][1], rgba_to_r_g_b_a(data.colour[i]))
		end
		cairo_set_source (cr, pat)
		cairo_pattern_destroy(pat)
	end

	cairo_set_operator(cr,t_operators[data.operator])

	if data.border>0 then
		cairo_close_path(cr)
		if data.dash ~= nil then cairo_set_dash(cr, data.dash, 1, 0.0) end
		cairo_set_line_width(cr,data.border)
		cairo_stroke(cr)
	else
		cairo_fill(cr)
	end

	cairo_restore(cr)
end

-------------------------------------------------------------------------------
--                                                                         MAIN
function conky_main(color, theme, n_cpu, swap, clock_theme, player, player_theme)

	if conky_window == nil then return end

	local cs = cairo_xlib_surface_create(conky_window.display, conky_window.drawable, conky_window.visual, conky_window.width, conky_window.height)

	cr = cairo_create(cs)

	local updates=tonumber(conky_parse('${updates}'))
	if updates>5 then

	if color == "white" then
		bgc = 0xffffff -- the colour of the base ring.
		fgc = 0xffffff -- the colour of the indicator part of the ring.
		bga = 0.2 --the alpha value of the base ring.
		fga = 0.8 -- the alpha value of the indicator part of the ring.
	else
		bgc = 0x1e1c1a -- the colour of the base ring.
		fgc = 0x1e1c1a -- the colour of the indicator part of the ring.
		bga = 0.6 -- the alpha value of the base ring.
		fga = 0.8 -- the alpha value of the indicator part of the ring.
	end

	local theme = ("0x" .. theme)
	local w = conky_window.width
	local h = conky_window.height
	local hori_space = 190
	local vert_space = 46
	local xp = hori_space
	local yp = vert_space

	-- CPU
	for i=1,n_cpu do
		cpu_number = ("cpu" .. i)
		settings = {--CPU GRAPH CPU1
			value=tonumber(conky_parse("${cpu " .. cpu_number .. "}")),
			value_max=100              ,
			x=xp                       , y=yp                        ,
			graph_radius=20            ,
			graph_thickness=10         ,
			graph_start_angle=180      ,
			graph_unit_angle=1.85      , graph_unit_thickness=2.7    ,
			graph_bg_colour=bgc        , graph_bg_alpha=bga          ,
			graph_fg_colour=fgc        , graph_fg_alpha=fga          ,
			hand_fg_colour=fgc         , hand_fg_alpha=0.0           ,
			txt_radius=35              ,
			txt_weight=1               , txt_size=8.0                ,
			txt_fg_colour=fgc          , txt_fg_alpha=0              ,
			graduation_radius=28       ,
			graduation_thickness=0     , graduation_mark_thickness=1 ,
			graduation_unit_angle=27   ,
			graduation_fg_colour=theme , graduation_fg_alpha=0.3     ,
			caption=''                 ,
			caption_weight=1           , caption_size=10.0           ,
			caption_fg_colour=fgc      , caption_fg_alpha=fga        ,
		};draw_gauge_ring(settings)
		yp = yp + 64
	end

	-- MEMORY
	settings = {--MEMPERC GRAPH
		value=tonumber(conky_parse("${memperc}")),
		value_max=100            ,
		x=xp                     , y=yp                        ,
		graph_radius=20          ,
		graph_thickness=10       ,
		graph_start_angle=180    ,
		graph_unit_angle=1.85    , graph_unit_thickness=2.7    ,
		graph_bg_colour=bgc      , graph_bg_alpha=bga          ,
		graph_fg_colour=fgc      , graph_fg_alpha=fga          ,
		hand_fg_colour=fgc       , hand_fg_alpha=0.0           ,
		txt_radius=35            ,
		txt_weight=1             , txt_size=8.0                ,
		txt_fg_colour=fgc        , txt_fg_alpha=0.0            ,
		graduation_radius=22     ,
		graduation_thickness=0   , graduation_mark_thickness=2 ,
		graduation_unit_angle=27 ,
		graduation_fg_colour=fgc , graduation_fg_alpha=0.5     ,
		caption=''               ,
		caption_weight=1         , caption_size=10.0           ,
		caption_fg_colour=fgc    , caption_fg_alpha=fga        ,
	};draw_gauge_ring(settings)

	-- SWAP
	if swap == "on" then
		yp = yp + 64
		settings = {--SWAP FILESYSTEM USED GRAPH
			value=tonumber(conky_parse("${swapperc}")),
			value_max=100            ,
			x=xp                     , y=yp                        ,
			graph_radius=20          ,
			graph_thickness=10       ,
			graph_start_angle=180    ,
			graph_unit_angle=1.85    , graph_unit_thickness=2.7    ,
			graph_bg_colour=bgc      , graph_bg_alpha=bga          ,
			graph_fg_colour=fgc      , graph_fg_alpha=fga          ,
			hand_fg_colour=fgc       , hand_fg_alpha=0.0           ,
			txt_radius=35            ,
			txt_weight=1             , txt_size=8.0                ,
			txt_fg_colour=fgc        , txt_fg_alpha=0              ,
			graduation_radius=22     ,
			graduation_thickness=0   , graduation_mark_thickness=2 ,
			graduation_unit_angle=27 ,
			graduation_fg_colour=fgc , graduation_fg_alpha=0.5     ,
			caption=''               ,
			caption_weight=1         , caption_size=10.0           ,
			caption_fg_colour=fgc    , caption_fg_alpha=fga        ,
		};draw_gauge_ring(settings)
	end

	-- CLOCK
	if clock_theme == "cairo" then
		yp = yp + 64
		settings = {--CLOCK HANDS
			xc = 154          ,
			yc = yp           ,
			colour = bgc      ,
			alpha = 1         ,
			show_secs = false ,
			size = 30         ,
		};clock_hands(settings)
		settings = {--SECONDS
			value=tonumber(conky_parse("${time %S}")),
			value_max = 60  ,
			x = 154         , y = yp          ,
			bg_colour = bgc , bg_alpha = bga  ,
			fg_colour = fgc , fg_alpha = fga  ,
			radius =20      , thickness = 5   ,
			start_angle = 0 , end_angle = 360 ,
			lr = 0          ,
		};draw_ring(settings)
	elseif clock_theme == "bigcairo" then
		yp = yp + 64 + 20
		settings = {--CLOCK HANDS
			xc = 124         ,
			yc = yp          ,
			colour = bgc     ,
			alpha = 1        ,
			show_secs = true ,
			size = 60        ,
		};clock_hands(settings)
		settings = {--DAYS
			value=tonumber(conky_parse("${time %d}")),
			value_max = 31    ,
			x = 124           , y = yp          ,
			bg_colour = bgc   , bg_alpha = bga  ,
			fg_colour = fgc   , fg_alpha = fga  ,
			radius =50        , thickness = 5   ,
			start_angle = 215 , end_angle = 325 ,
			lr = 0            ,
		};draw_ring(settings)
		settings = {--MONTHS
			value=tonumber(conky_parse("${time %m}")),
			value_max = 12   ,
			x = 124          , y = yp          ,
			bg_colour = bgc  , bg_alpha = bga  ,
			fg_colour = fgc  , fg_alpha = fga  ,
			radius = 50      , thickness = 5   ,
			start_angle = 35 , end_angle = 145 ,
			lr = 0           ,
		};draw_ring(settings)
		settings = {--SECONDS
			value=tonumber(conky_parse("${time %S}")),
			value_max = 60  ,
			x = 124         , y = yp          ,
			bg_colour = bgc , bg_alpha = bga  ,
			fg_colour = fgc , fg_alpha = fga  ,
			radius =40      , thickness = 10  ,
			start_angle = 0 , end_angle = 360 ,
			lr = 0          ,
		};draw_ring(settings)
		yp = yp + 22
	end

	yp = yp + 64
	-- DISKS
	disks = {'/', '/home'}
	for i, partitions in ipairs(disks) do
		settings = {--FILESYSTEM USED GRAPH
			value=tonumber(conky_parse("${fs_used_perc " .. partitions .. "}")),
			value_max=100            ,
			x=xp                     , y=yp                        ,
			graph_radius=20          ,
			graph_thickness=10       ,
			graph_start_angle=180    ,
			graph_unit_angle=1.85    , graph_unit_thickness=2.7    ,
			graph_bg_colour=bgc      , graph_bg_alpha=bga          ,
			graph_fg_colour=fgc      , graph_fg_alpha=fga          ,
			hand_fg_colour=fgc       , hand_fg_alpha=0.0           ,
			txt_radius=35            ,
			txt_weight=1             , txt_size=8.0                ,
			txt_fg_colour=fgc        , txt_fg_alpha=0              ,
			graduation_radius=23     ,
			graduation_thickness=0   , graduation_mark_thickness=2 ,
			graduation_unit_angle=27 ,
			graduation_fg_colour=fgc , graduation_fg_alpha=0.5     ,
			caption=''               ,
			caption_weight=1         , caption_size=10.0           ,
			caption_fg_colour=fgc    , caption_fg_alpha=fga        ,
		};draw_gauge_ring(settings)
		yp = yp + 64
	end

	-- PLAYERS
	if player == "Banshee" or player == "Clementine" or player == "Rhythmbox" then
		if player_theme == "cairo" then
			settings = {
				value=get_music_percent(player) ,
				value_max = 100   ,
				x = 154           , y = yp          ,
				bg_colour = bgc   , bg_alpha = bga  ,
				fg_colour = theme , fg_alpha = fga  ,
				radius =10        , thickness = 20  ,
				start_angle = 0   , end_angle = 360 ,
				lr = 0            ,
			};draw_ring(settings)
			settings = {
				value=get_music_percent(player),
				value_max = 100 ,
				x = 154         , y = yp          ,
				bg_colour = bgc , bg_alpha = 0.4  ,
				fg_colour = fgc , fg_alpha = 0.2  ,
				radius =20      , thickness = 1   ,
				start_angle = 0 , end_angle = 360 ,
				lr = 0          ,
			};draw_ring(settings)
		elseif player_theme == "cairocover" then
			settings = {
				value=get_music_percent(player),
				value_max = 100   ,
				x = 174           , y = yp-18       ,
				bg_colour = bgc   , bg_alpha = 0.4  ,
				fg_colour = theme , fg_alpha = 1    ,
				radius =5         , thickness = 11  ,
				start_angle = 0   , end_angle = 360 ,
				lr = 0            ,
			};draw_ring(settings)
			settings = {
				value=get_music_percent(player),
				value_max = 100 ,
				x = 174         , y = yp-18       ,
				bg_colour = bgc , bg_alpha = 0.6  ,
				fg_colour = fgc , fg_alpha = 0.2  ,
				radius =11      , thickness = 2   ,
				start_angle = 0 , end_angle = 360 ,
				lr = 0          ,
			};draw_ring(settings)
		else
		settings = {--PLAYERS
			value=get_music_percent(player),
			value_max=100            ,
			x=xp                     , y=yp                        ,
			graph_radius=20          ,
			graph_thickness=10       ,
			graph_start_angle=180    ,
			graph_unit_angle=1.85    , graph_unit_thickness=2.7    ,
			graph_bg_colour=bgc      , graph_bg_alpha=bga          ,
			graph_fg_colour=fgc      , graph_fg_alpha=fga          ,
			hand_fg_colour=fgc       , hand_fg_alpha=0.0           ,
			txt_radius=35            ,
			txt_weight=1             , txt_size=8.0                ,
			txt_fg_colour=fgc        , txt_fg_alpha=0              ,
			graduation_radius=23     ,
			graduation_thickness=0   , graduation_mark_thickness=2 ,
			graduation_unit_angle=27 ,
			graduation_fg_colour=fgc , graduation_fg_alpha=0.5     ,
			caption=''               ,
			caption_weight=1         , caption_size=10.0           ,
			caption_fg_colour=fgc    , caption_fg_alpha=fga        ,
		};draw_gauge_ring(settings)
		end
	end

	end-- if updates>5
	cairo_destroy(cr)
	cairo_surface_destroy(cs)
	cr=nil
end-- end main function
