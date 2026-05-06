import { Injectable, ConflictException, UnauthorizedException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';
import { User } from './user.entity';
import { RegisterDto } from './dto/register.dto';
import { LoginDto } from './dto/login.dto';

/**
 * Service d'authentification — contient toute la logique métier liée aux utilisateurs.
 *
 * En NestJS, un Service est une classe injectable (@Injectable) qui encapsule
 * la logique métier. Le Controller reçoit les requêtes HTTP, valide les données
 * via les DTOs, puis délègue le traitement au Service.
 * Cette séparation facilite les tests unitaires : on peut tester le Service
 * sans démarrer un serveur HTTP.
 */
@Injectable()
export class AuthService {
  constructor(
    // @InjectRepository injecte le dépôt TypeORM pour l'entité User
    // C'est l'équivalent du QuerySet Django — il expose find(), save(), remove()...
    @InjectRepository(User) private userRepo: Repository<User>,

    // JwtService fourni par @nestjs/jwt — signe et vérifie les tokens JWT
    private jwtService: JwtService,
  ) {}

  /**
   * Crée un nouveau compte utilisateur (US03).
   * Vérifie l'unicité de l'email, hache le mot de passe, puis insère en base.
   */
  async register(dto: RegisterDto) {
    // On vérifie en base si l'email existe déjà avant d'insérer
    const existing = await this.userRepo.findOneBy({ email: dto.email });
    if (existing) throw new ConflictException('Email déjà utilisé.');

    // bcrypt avec un coût de 12 itérations — bon équilibre sécurité/performance
    // Plus le chiffre est élevé, plus le hash est lent à calculer (protection brute-force)
    const password = await bcrypt.hash(dto.password, 12);

    // create() instancie l'entité sans l'écrire en base — save() fait l'INSERT
    const user = this.userRepo.create({ ...dto, password });
    await this.userRepo.save(user);

    // On ne retourne jamais le hash du mot de passe dans la réponse
    return { id: user.id, email: user.email, username: user.username };
  }

  /**
   * Authentifie un utilisateur et retourne un token JWT (US04).
   * Le message d'erreur est volontairement générique pour ne pas indiquer
   * si c'est l'email ou le mot de passe qui est incorrect (énumération d'utilisateurs).
   */
  async login(dto: LoginDto) {
    const user = await this.userRepo.findOneBy({ email: dto.email });

    // Même message que pour le mot de passe incorrect — sécurité par opacité
    if (!user) throw new UnauthorizedException('Identifiants invalides.');

    // bcrypt.compare compare le mot de passe en clair avec le hash stocké
    const valid = await bcrypt.compare(dto.password, user.password);
    if (!valid) throw new UnauthorizedException('Identifiants invalides.');

    // Le payload JWT contient l'id (sub = subject, convention JWT RFC 7519) et l'email
    // Ce payload sera disponible dans req.user après validation par JwtStrategy
    const token = this.jwtService.sign({ sub: user.id, email: user.email });

    return {
      access_token: token,
      user: { id: user.id, email: user.email, username: user.username },
    };
  }

  /**
   * Retourne le profil de l'utilisateur connecté (US05 — espace personnel).
   * Appelé par GET /api/auth/me après validation du JWT par le guard.
   */
  async getProfile(userId: number) {
    const user = await this.userRepo.findOneBy({ id: userId });
    if (!user) throw new UnauthorizedException();
    return { id: user.id, email: user.email, username: user.username };
  }
}
