import langrisser

dir_solid_pic = 'pics\/'
for i in range(660,668):
    langrisser.window_capture(dir_solid_pic+'19_3_ball.bmp', i, 352, i+24,377)
    rms1 = langrisser.rms_difference(dir_solid_pic+'19_1_ball.bmp', dir_solid_pic+'19_3_ball.bmp')
    rms2 = langrisser.rms_difference(dir_solid_pic+'19_2_ball.bmp', dir_solid_pic+'19_3_ball.bmp')
    print(i, rms1, rms2)
