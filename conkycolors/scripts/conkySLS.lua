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
--                                                             get_weather_info
-- return weather info
--
function get_weather_info(data, day, area_code)
	local f = assert(io.popen("conky-colors --systemdir"))
	local s = assert(f:read('*l'))
	f:close()
	f = assert(io.popen("sh " .. s .. "/bin/conkyForecast --location=" .. area_code .. " --datatype=" .. data .. " --startday=" .. day)) -- runs command
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
function conky_main(color, theme, drawbg, weather_code)

	if conky_window == nil then return end

	local cs = cairo_xlib_surface_create(conky_window.display, conky_window.drawable, conky_window.visual, conky_window.width, conky_window.height)

	cr = cairo_create(cs)

	local updates=tonumber(conky_parse('${updates}'))
	if updates>5 then

	-- BACKGROUND COLOR
	if color == "white" then
		bgc = 0x1e1c1a
		bga = 0.7
	else
		bgc = 0xffffff
		bga = 0.4
	end

	local theme = ("0x" .. theme)
	local w = conky_window.width
	local h = conky_window.height
	local hori_space = w*0.07
	local vert_space = h*0.5
	local xp = 24
	local yp = 70

	-- BACKGROUND
	if drawbg == "on" then
	settings={
		x=0+10   , y=0 ,
		w=w-10   , h=h ,
		border=1 ,
		colour={{0,bgc,0.2},},
	};draw_box(settings)
	settings={
		x=0+10 , y=0 ,
		w=w-10 , h=h ,
		colour={{0.5,bgc,bga},{1,bgc,bga+0.05},},
		linear_gradient={0,0,w/2,h/2},
	};draw_box(settings)
	settings={
		x=0+9 , y=0 ,
		w=5   , h=h ,
		colour={{0,theme,1},},
	};draw_box(settings)
	settings={
		x=0+14 , y=h-1 ,
		w=w   , h=1 ,
		colour={{0,bgc,0.2},},
	};draw_box(settings)

	end

	-- IMAGE
	if color == "white" then
		image = cairo_image_surface_create_from_png ("/usr/share/conkycolors/icons/SLS/Cover.png")
	else
		image = cairo_image_surface_create_from_png ("/usr/share/conkycolors/icons/SLS/Cover_white.png")
	end
	cairo_set_source_surface (cr, image, -5, 90)
	cairo_paint (cr);
	cairo_surface_destroy (image);

	-- WEATHER ICON
	image = cairo_image_surface_create_from_png (get_weather_info ("WI", 0, weather_code))
	cairo_set_source_surface (cr, image, 125, 85)
	cairo_paint (cr);
	cairo_surface_destroy (image);

	-- THEME
	if color == "white" then
		bgc = 0xffffff
		fgc = 0xffffff
		bga = 0.5
		fga = 0.8
	else
		bgc = 0x1e1c1a
		fgc = 0x1e1c1a
		bga = 0.5
		fga = 0.8
	end

	-- CPU
	for i=1,10 do
		settings={
			value=tonumber(conky_parse("${cpu cpu0}")),
			value_max=100          ,
			x=xp                   , y=yp           ,
			divisions=10           ,
			div_width=4.5          , div_height=4.5 ,
			div_gap=0.5            ,
			bg_alpha=bga           , bg_color=bgc   ,
			fg_alpha=1             ,
			st_color=theme         ,
			mid_color=theme        ,
			end_color=theme        ,
			orientation="vertical" ,
		};draw_gauge_bars(settings)
		xp = xp + 5
	end
	settings = {
		txt=conky_parse("${cpu cpu0}") .. "%",
		x=xp-45           , y=yp+15        ,
		txt_weight=1      , txt_size=14    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		txt="CPU"         ,
		x=xp-17           , y=yp+10          ,
		txt_weight=0      , txt_size=8       ,
		txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
	};display_text(settings)
	xp = xp + 5

	-- MEMORY
	for i=1,10 do
		settings={
			value=tonumber(conky_parse("${memperc}")),
			value_max=100          ,
			x=xp                   , y=yp           ,
			divisions=10           ,
			div_width=4.5          , div_height=4.5 ,
			div_gap=0.5            ,
			bg_alpha=bga           , bg_color=bgc   ,
			fg_alpha=1             ,
			st_color=theme         ,
			mid_color=theme        ,
			end_color=theme        ,
			orientation="vertical" ,
		};draw_gauge_bars(settings)
		xp = xp + 5
	end
	settings = {
		txt=tonumber(conky_parse("${memperc}")) .. "%",
		x=xp-45           , y=yp+15        ,
		txt_weight=1      , txt_size=14    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		txt="RAM"         ,
		x=xp-17           , y=yp+10          ,
		txt_weight=0      , txt_size=8       ,
		txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
	};display_text(settings)
	xp = xp + 5

	-- SWAP
	for j=1,10 do
		settings={
			value=tonumber(conky_parse("${swapperc}")),
			value_max=100          ,
			x=xp                   , y=yp           ,
			divisions=10           ,
			div_width=4.5          , div_height=4.5 ,
			div_gap=0.5            ,
			bg_alpha=bga           , bg_color=bgc   ,
			fg_alpha=1             ,
			st_color=theme         ,
			mid_color=theme        ,
			end_color=theme        ,
			orientation="vertical" ,
		};draw_gauge_bars(settings)
		xp = xp + 5
	end
	settings = {
		txt=tonumber(conky_parse("${swapperc}")) .. '%',
		x=xp-45           , y=yp+15        ,
		txt_weight=1      , txt_size=14    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		txt='SWP'         ,
		x=xp-17           , y=yp+10          ,
		txt_weight=0      , txt_size=8       ,
		txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
	};display_text(settings)
	xp = xp + 5

	-- CPU TEMP
	for i=1,10 do
		settings={
			value=tonumber(conky_parse("${execi 30 sensors | grep 'Core 0' | cut -c16-17}")),
			value_max=100          ,
			x=xp                   , y=yp           ,
			divisions=10           ,
			div_width=4.5          , div_height=4.5 ,
			div_gap=0.5            ,
			bg_alpha=bga           , bg_color=bgc   ,
			fg_alpha=1             ,
			st_color=theme         ,
			mid_color=theme        ,
			end_color=theme        ,
			orientation="vertical" ,
		};draw_gauge_bars(settings)
		xp = xp + 5
	end
	settings = {
		txt=conky_parse("${execi 30 sensors | grep 'Core 1' | cut -c16-17}") .. '°C',
		x=xp-45           , y=yp+15        ,
		txt_weight=1      , txt_size=14    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		txt='SYS'         ,
		x=xp-15           , y=yp+10          ,
		txt_weight=0      , txt_size=8       ,
		txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
	};display_text(settings)

	yp=yp+145
	xp=21

	-- BATTERY
	for i=1,2 do
		settings={
			value=tonumber(conky_parse("${battery_percent BAT0}")),
			value_max=100            ,
			x=xp                     , y=yp           ,
			divisions=29             ,
			div_width=4.5            , div_height=4.5 ,
			div_gap=0.5              ,
			bg_alpha=bga             , bg_color=bgc   ,
			fg_alpha=1               ,
			st_color=theme           ,
			mid_color=theme          ,
			end_color=theme          ,
			orientation="horizontal" ,
		};draw_gauge_bars(settings)
		yp = yp + 5
	end
	for i=1,4 do
		settings={
			value=tonumber(conky_parse("${battery_percent BAT0}")),
			value_max=100            ,
			x=xp                     , y=yp           ,
			divisions=30             ,
			div_width=4.5            , div_height=4.5 ,
			div_gap=0.5              ,
			bg_alpha=bga             , bg_color=bgc   ,
			fg_alpha=1               ,
			st_color=theme           ,
			end_color=theme          ,
			mid_color=theme          ,
			orientation="horizontal" ,
		};draw_gauge_bars(settings)
		yp = yp + 5
	end
	for i=1,2 do
		settings={
			value=tonumber(conky_parse("${battery_percent BAT0}")),
			value_max=100            ,
			x=xp                     , y=yp           ,
			divisions=29             ,
			div_width=4.5            , div_height=4.5 ,
			div_gap=0.5              ,
			bg_alpha=bga             , bg_color=bgc   ,
			fg_alpha=1               ,
			st_color=theme           ,
			mid_color=theme          ,
			end_color=theme          ,
			orientation="horizontal" ,
		};draw_gauge_bars(settings)
		yp = yp + 5
	end
	settings = {
		txt=conky_parse("${battery_percent BAT0}") .. '%',
		x=200             , y=235          ,
		txt_weight=1      , txt_size=14    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		txt='ON BATTERY'  ,
		x=185             , y=245            ,
		txt_weight=0      , txt_size=8       ,
		txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
	};display_text(settings)

	yp=yp+20
	xp=25

	-- PROCESSES ICON
	settings = {
		txt='n', font='conkySymbols',
		x=xp+12           , y=yp+25        ,
		txt_weight=0      , txt_size=30    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)

	yp=yp+100
	xp=25

	-- DISKS
	disks = {'/', '/home'}
	disksLabel = {'ROOT', 'HOME'}
	for i, partitions in ipairs(disks) do
		for j=1,10 do
			settings={
				value=tonumber(conky_parse("${fs_used_perc " .. partitions .. "}")),
				value_max=100          ,
				x=xp                   , y=yp           ,
				divisions=10           ,
				div_width=4.5          , div_height=4.5 ,
				div_gap=0.5            ,
				bg_alpha=bga           , bg_color=bgc   ,
				fg_alpha=1             ,
				st_color=theme         ,
				end_color=theme        ,
				mid_color=theme        ,
				orientation="vertical" ,
			};draw_gauge_bars(settings)
			xp = xp + 5
		end
		xp = xp + 55
		settings = {
			txt=conky_parse("${fs_used_perc " .. partitions .. "}") .. '%',
			x=xp-43           , y=yp-28        ,
			txt_weight=1      , txt_size=14    ,
			txt_fg_colour=bgc , txt_fg_alpha=1 ,
		};display_text(settings)
		settings = {
			txt=disksLabel[i] ,
			x=xp-45           , y=yp-42        ,
			txt_weight=0      , txt_size=10    ,
			txt_fg_colour=bgc , txt_fg_alpha=1 ,
		};display_text(settings)
		settings = {
			txt='F: ' .. conky_parse("${fs_free " .. partitions .. "}"),
			x=xp-45           , y=yp-18          ,
			txt_weight=0      , txt_size=8       ,
			txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
		};display_text(settings)
		settings = {
			txt='U: ' .. conky_parse("${fs_used " .. partitions .. "}"),
			x=xp-45           , y=yp-8           ,
			txt_weight=0      , txt_size=8       ,
			txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
		};display_text(settings)
	end

	yp=yp+72
	xp=25

	-- MAIL ICON
	settings = {
		txt='c', font='conkySymbols',
		x=xp+12           , y=yp-25        ,
		txt_weight=0      , txt_size=30    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		value=100         , value_max = 100 ,
		x = xp+25         , y = yp-50       ,
		bg_colour = bgc   , bg_alpha = 0.4  ,
		fg_colour = theme , fg_alpha = 1    ,
		radius = 4        , thickness = 11  ,
		start_angle = 0   , end_angle = 360 ,
		lr = 0            ,
	};draw_ring(settings)

	yp=yp+50

	-- WIRELESS SIGNAL
	j=0
	for i=1,6 do
		j = j + 1
		settings={
			value=tonumber(conky_parse("${wireless_link_qual_perc wlan0}")),
			value_max=100          ,
			x=xp                   , y=yp-30        ,
			divisions=j            ,
			div_width=4.5          , div_height=4.5 ,
			div_gap=0.5            ,
			bg_alpha=bga           , bg_color=bgc   ,
			fg_alpha=1             ,
			st_color=theme         ,
			mid_color=theme        ,
			end_color=theme        ,
			orientation="vertical" ,
		};draw_gauge_bars(settings)
		xp = xp + 5
	end
	wireless_name = conky_parse("${wireless_link_qual_perc wlan0}")
	if wireless_name == 'unk' then
		wireless_name = '  no'
	else
		wireless_name = wireless_name .. '%'
	end
	settings = {
		txt=wireless_name,
		x=xp-25           , y=yp-15        ,
		txt_weight=1      , txt_size=14    ,
		txt_fg_colour=bgc , txt_fg_alpha=1 ,
	};display_text(settings)
	settings = {
		txt='SIGNAL'      ,
		x=xp-27           , y=yp-5           ,
		txt_weight=0      , txt_size=8       ,
		txt_fg_colour=bgc , txt_fg_alpha=0.6 ,
	};display_text(settings)

	end-- if updates>5
	cairo_destroy(cr)
	cairo_surface_destroy(cs)
	cr=nil
end-- end main function
