class Settings:
    name = 'Space Invaders'
    screen_size = width, height = (800, 400)

    player_surf = 'ship.bmp'
    player_pos = (screen_size[0] / 2, screen_size[1])
    p_lives_size = w_s, h_s = (20, 20)
    p_lives_pos = x_l, y_l = (5, 5)
    p_lives_color = 'Green'

    bullet_size = (4.5, 12)
    bullet_i_size = (3.5, 8.5)
    bullet_color = 'Red'
    bull_inv_color = 'Blue'

    alien_surf = 'alien.bmp'
    alien_size = width_a, height_a = (50, 25)
    aliens = alien_rows, alien_columns = (3, 9)

    blocks_color = 'Grey'
    b_s = (5, 5)
    b_p = (400, 300)
