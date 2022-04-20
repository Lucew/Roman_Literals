// stolen from:
// http://www.novaroma.org/via_romana/numbers.html

function Level(i, v, x)
        {
        this.i = i;
        this.v = v;
        this.x = x
        }

levels = new Array();

levels[0] = new Level('I', 'V', 'X');
levels[1] = new Level('X', 'L', 'C');
levels[2] = new Level('C', 'D', 'M');




function calcDigit(d, l)
        {
        if (l > 2)
                {
                str = '';
                for (var m = 1; m <= d * Math.pow(10, l - 3) ; m++)
                        str += 'M';
                return str
                }

        else
                if (d == 1)
                        return levels[l].i
                else
                        if (d == 2)
                                return levels[l].i + levels[l].i
                        else
                                if (d == 3)
                                        return levels[l].i + levels[l].i + levels[l].i
                                else
                                        if (d == 4)
                                                return levels[l].i + levels[l].v
                                        else
                                                if (d == 5)
                                                        return levels[l].v
                                                else
                                                        if (d == 6)
                                                                return levels[l].v + levels[l].i
                                                        else
                                                                if (d == 7)
                                                                        return levels[l].v + levels[l].i + levels[l].i
                                                                else
                                                                        if (d == 8)
                                                                                return levels[l].v + levels[l].i + levels[l].i + levels[l].i
                                                                        else
                                                                                if (d == 9)
                                                                                        return levels[l].i + levels[l].x
                                                                                else
                                                                                        return ''
        }

function toRoman(n)
        {
        var r = ''
        for (var c = 0; c < n.length; c++)
                r += calcDigit(eval(n.charAt(c)), n.length - c - 1);
        return r
        }

function fromRoman(n)
        {
        var r = 0

        for (var c = 0; c < n.length; c++)
                {
                var chr = n.charAt(c).toLowerCase();
                if (c < n.length - 1)
                        var next = n.charAt(c + 1).toLowerCase()
                else
                        var next = '';

                if (c > 0)
                        var prev = n.charAt(c - 1).toLowerCase()
                else
                        var prev = '';

                if (chr == 'i')
                        {
                        if (next == 'v')
                                r += 4
                        else
                                if (next == 'x')
                                        r += 9
                                else
                                        r += 1;
                        continue
                        }

                if (chr == 'v')
                        {
                        if (prev != 'i')
                                r += 5;
                        continue
                        }

                if (chr == 'x')
                        {
                        if (prev != 'i')
                                if (next == 'l')
                                        r += 40
                                else
                                        if (next == 'c')
                                                r += 90
                                        else
                                                r += 10;
                        continue
                        }

                if (chr == 'l')
                        {
                        if (prev != 'x')
                                r += 50;
                        continue
                        }

                if (chr == 'c')
                        {
                        if (prev != 'x')
                                if (next == 'd')
                                        r += 400
                                else
                                        if (next == 'm')
                                                r += 900
                                        else
                                                r += 100;
                        continue
                        }

                if (chr == 'd')
                        {
                        if (prev != 'c')
                                r += 500;
                        continue
                        }

                if (chr == 'm')
                        {
                        if (prev != 'c')
                                r += 1000;
                        continue

                        }
                }

        return r

        }
